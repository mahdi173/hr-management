"""Assign Employee to Shift Use Case - Business logic for shift assignments"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta

from ..shared.shift_dto import ShiftAssignmentCreate, ShiftAssignmentResponse
from ....repositories.shift_repository import ShiftRepository, ShiftAssignmentRepository
from ....repositories.employee_repository import EmployeeRepository
from ....repositories.availability_repository import AvailabilityRepository
from ....repositories.absence_repository import AbsenceRepository
from ....models.shift import ShiftAssignment


class AssignEmployeeUseCase:
    """Use case for assigning an employee to a shift"""
    
    def __init__(self, db: Session):
        self.db = db
        self.shift_repo = ShiftRepository(db)
        self.assignment_repo = ShiftAssignmentRepository(db)
        self.employee_repo = EmployeeRepository(db)
        self.availability_repo = AvailabilityRepository(db)
        self.absence_repo = AbsenceRepository(db)
    
    def execute(self, assignment_data: ShiftAssignmentCreate) -> ShiftAssignmentResponse:
        """
        Assign an employee to a shift
        
        Business rules:
        - Shift must exist
        - Employee must exist and be active
        - Employee must not already be assigned to this shift
        - Employee must not have overlapping shift assignments
        - Employee must be available during shift time (check availability)
        - Employee must not have an approved absence during shift date
        - Shift must not exceed max_employees limit
        """
        # Validate shift exists
        shift = self.shift_repo.get_by_id(assignment_data.shift_id)
        if not shift:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shift with id {assignment_data.shift_id} not found"
            )
        
        # Validate employee exists and is active
        employee = self.employee_repo.get_by_id(assignment_data.employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with id {assignment_data.employee_id} not found"
            )
        if not employee.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Employee {employee.first_name} {employee.last_name} is not active"
            )
        
        # Check if already assigned
        existing = self.assignment_repo.get_by_employee_and_shift(
            assignment_data.employee_id,
            assignment_data.shift_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee is already assigned to this shift"
            )
        
        # Check for overlapping shifts
        has_conflict = self.assignment_repo.check_employee_conflict(
            employee_id=assignment_data.employee_id,
            shift_date=shift.date,
            start_time=shift.start_time,
            end_time=shift.end_time
        )
        if has_conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee has an overlapping shift assignment"
            )
        
        # Check availability (recurring or specific date)
        day_of_week = shift.date.weekday()  # Monday=0, Sunday=6
        is_available = self._check_availability(
            employee_id=assignment_data.employee_id,
            shift_date=shift.date,
            day_of_week=day_of_week,
            start_time=shift.start_time,
            end_time=shift.end_time
        )
        if not is_available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee is not available during this shift time"
            )
        
        # Check for approved absences
        absences = self.absence_repo.get_by_employee_and_date_range(
            employee_id=assignment_data.employee_id,
            start_date=shift.date,
            end_date=shift.date
        )
        approved_absences = [a for a in absences if a.status == "approved"]
        if approved_absences:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee has an approved absence during this shift date"
            )
        
        # Check max employees limit
        current_count = self.assignment_repo.count_assignments_for_shift(assignment_data.shift_id)
        if current_count >= shift.max_employees:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Shift has reached maximum capacity ({shift.max_employees} employees)"
            )
        
        # Create assignment
        assignment = ShiftAssignment(**assignment_data.model_dump())
        created_assignment = self.assignment_repo.create(assignment)
        
        return ShiftAssignmentResponse.model_validate(created_assignment)
    
    def _check_availability(
        self,
        employee_id: int,
        shift_date,
        day_of_week: int,
        start_time,
        end_time
    ) -> bool:
        """
        Check if employee is available during shift time
        
        Priority: specific date availability > recurring availability
        """
        # Check for specific date availability first
        specific_availabilities = self.availability_repo.get_by_specific_date(
            employee_id=employee_id,
            specific_date=shift_date
        )
        
        if specific_availabilities:
            # If specific date availabilities exist, check against them
            for avail in specific_availabilities:
                if not avail.is_active:
                    continue
                # Check if shift time is within availability window
                if avail.start_time <= start_time and avail.end_time >= end_time:
                    return True
            return False
        
        # Fall back to recurring availability
        recurring_availabilities = self.availability_repo.get_by_day(
            employee_id=employee_id,
            day_of_week=day_of_week
        )
        
        for avail in recurring_availabilities:
            if not avail.is_active:
                continue
            # Check if shift time is within availability window
            if avail.start_time <= start_time and avail.end_time >= end_time:
                return True
        
        # No matching availability found
        return False

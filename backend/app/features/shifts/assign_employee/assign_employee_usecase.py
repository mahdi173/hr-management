"""Assign Employee to Shift Use Case - Business logic for shift assignments"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta

from ..shared.shift_dto import ShiftAssignmentCreate, ShiftAssignmentResponse
from ..shared.conflict_service import ConflictDetectionService
from ..shared.compliance_service import ComplianceService
from ....repositories.shift_repository import ShiftRepository, ShiftAssignmentRepository
from ....repositories.employee_repository import EmployeeRepository
from ....models.shift import ShiftAssignment


class AssignEmployeeUseCase:
    """Use case for assigning an employee to a shift"""
    
    def __init__(self, db: Session):
        self.db = db
        self.shift_repo = ShiftRepository(db)
        self.assignment_repo = ShiftAssignmentRepository(db)
        self.employee_repo = EmployeeRepository(db)
        self.conflict_service = ConflictDetectionService(db)
        self.compliance_service = ComplianceService(db)
    
    def execute(self, assignment_data: ShiftAssignmentCreate) -> ShiftAssignmentResponse:
        """
        Assign an employee to a shift
        
        Business rules:
        - Shift must exist
        - Employee must exist and be active
        - Employee must not already be assigned to this shift
        - Employee must not have conflicts (overlapping shifts, unavailability, absences)
        - Employee must comply with labor rules (blocking rules)
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
        
        # Check for conflicts using dedicated service
        conflicts = self.conflict_service.check_all_conflicts(
            employee_id=assignment_data.employee_id,
            shift_date=shift.date,
            start_time=shift.start_time,
            end_time=shift.end_time
        )
        
        if conflicts:
            # Create persistent alerts for these conflicts
            self.conflict_service.notify_conflicts(conflicts, shift_id=assignment_data.shift_id)
            
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": "Scheduling conflict detected",
                    "conflicts": [c.model_dump() for c in conflicts]
                }
            )
        
        # Check for compliance violations
        compliance = self.compliance_service.validate_assignment(
            employee_id=assignment_data.employee_id,
            shift_date=shift.date,
            start_time=shift.start_time,
            end_time=shift.end_time
        )
        
        # Notify about all violations (errors and warnings)
        if compliance.errors or compliance.violations:
            self.compliance_service.notify_violations(
                compliance, 
                employee_id=assignment_data.employee_id,
                shift_id=assignment_data.shift_id
            )
        
        if compliance.errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Compliance validation failed (blocking)",
                    "errors": compliance.errors
                }
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

"""Get Working Hours Use Case - Business logic for tracking employee hours (US 1.8)"""

from typing import List
from datetime import date, datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..shared.shift_dto import HoursSummary, ShiftWithHours
from ....repositories.shift_repository import ShiftAssignmentRepository
from ....repositories.employee_repository import EmployeeRepository
from ....repositories.contract_type_repository import ContractTypeRepository


class GetHoursUseCase:
    """Use case for retrieving working hours summaries and overtime"""
    
    def __init__(self, db: Session):
        self.db = db
        self.assignment_repo = ShiftAssignmentRepository(db)
        self.employee_repo = EmployeeRepository(db)
        self.contract_type_repo = ContractTypeRepository(db)
    
    def execute(
        self,
        employee_id: int,
        start_date: date,
        end_date: date
    ) -> HoursSummary:
        """
        Calculate working hours summary for an employee in a date range
        
        Returns total hours, regular hours, and overtime hours
        """
        # Validate employee exists
        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with id {employee_id} not found"
            )
        
        # Validate date range
        if start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="start_date must be before or equal to end_date"
            )
        
        # Get hours summary from repository
        hours_data = self.assignment_repo.get_hours_by_employee_and_period(
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date
        )
        
        return HoursSummary(
            employee_id=employee_id,
            period_start=start_date,
            period_end=end_date,
            **hours_data
        )
    
    def get_overtime_details(
        self,
        employee_id: int,
        start_date: date = None,
        end_date: date = None
    ) -> List[ShiftWithHours]:
        """
        Get detailed list of overtime shifts for an employee
        
        Returns list of shifts marked as overtime with calculated hours
        """
        # Validate employee exists
        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with id {employee_id} not found"
            )
        
        # Get overtime assignments
        overtime_assignments = self.assignment_repo.get_overtime_shifts(
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date
        )
        
        # Build response with calculated hours
        result = []
        for assignment in overtime_assignments:
            shift = assignment.shift
            
            # Calculate duration in hours
            start_dt = datetime.combine(shift.date, shift.start_time)
            end_dt = datetime.combine(shift.date, shift.end_time)
            duration = (end_dt - start_dt).total_seconds() / 3600
            
            result.append(ShiftWithHours(
                shift_id=shift.id,
                date=shift.date,
                start_time=shift.start_time,
                end_time=shift.end_time,
                duration_hours=round(duration, 2),
                is_overtime=assignment.is_overtime,
                assignment_type=assignment.assignment_type
            ))
        
        return result

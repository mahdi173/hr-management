"""Get Shifts Use Case - Business logic for retrieving shifts"""

from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session

from ..shared.shift_dto import ShiftResponse
from ....repositories.shift_repository import ShiftRepository


class GetShiftsUseCase:
    """Use case for retrieving shifts with various filters"""
    
    def __init__(self, db: Session):
        self.db = db
        self.shift_repo = ShiftRepository(db)
    
    def execute(
        self,
        schedule_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        employee_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
        include_assignments: bool = False
    ) -> List[ShiftResponse]:
        """
        Get shifts with optional filters
        
        Filters:
        - schedule_id: Get shifts for a specific schedule
        - start_date/end_date: Get shifts within date range
        - employee_id: Get shifts assigned to a specific employee
        - skip/limit: Pagination
        - include_assignments: Load shift assignments
        """
        if employee_id:
            # Get shifts assigned to employee
            shifts = self.shift_repo.get_by_employee(
                employee_id=employee_id,
                start_date=start_date,
                end_date=end_date,
                skip=skip,
                limit=limit
            )
        elif schedule_id:
            # Get shifts for schedule
            shifts = self.shift_repo.get_by_schedule(
                schedule_id=schedule_id,
                skip=skip,
                limit=limit,
                include_assignments=include_assignments
            )
        elif start_date and end_date:
            # Get shifts in date range
            shifts = self.shift_repo.get_by_date_range(
                start_date=start_date,
                end_date=end_date,
                skip=skip,
                limit=limit,
                include_assignments=include_assignments
            )
        else:
            # Get all shifts (paginated)
            shifts = self.shift_repo.get_all(skip=skip, limit=limit)
        
        return [ShiftResponse.model_validate(shift) for shift in shifts]
    
    def get_one(self, shift_id: int, include_assignments: bool = False) -> Optional[ShiftResponse]:
        """Get a single shift by ID"""
        if include_assignments:
            shift = self.shift_repo.get_with_assignments(shift_id)
        else:
            shift = self.shift_repo.get_by_id(shift_id)
        
        if shift:
            return ShiftResponse.model_validate(shift)
        return None

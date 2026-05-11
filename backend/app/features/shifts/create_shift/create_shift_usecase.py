"""Create Shift Use Case - Business logic for creating shifts"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..shared.shift_dto import ShiftCreate, ShiftResponse
from ....repositories.shift_repository import ShiftRepository
from ....repositories.schedule_repository import ScheduleRepository
from ....repositories.role_repository import RoleRepository
from ....models.shift import Shift


class CreateShiftUseCase:
    """Use case for creating a new shift"""
    
    def __init__(self, db: Session):
        self.db = db
        self.shift_repo = ShiftRepository(db)
        self.schedule_repo = ScheduleRepository(db)
        self.role_repo = RoleRepository(db)
    
    def execute(self, shift_data: ShiftCreate) -> ShiftResponse:
        """
        Create a new shift
        
        Business rules:
        - Schedule must exist
        - Required role must exist (if provided)
        - Shift date must be within schedule date range
        - min_employees and max_employees must be valid
        """
        # Validate schedule exists
        schedule = self.schedule_repo.get_by_id(shift_data.schedule_id)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Schedule with id {shift_data.schedule_id} not found"
            )
        
        # Validate shift date is within schedule range
        if shift_data.date < schedule.start_date or shift_data.date > schedule.end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Shift date must be between {schedule.start_date} and {schedule.end_date}"
            )
        
        # Validate required role exists (if provided)
        if shift_data.required_role_id:
            role = self.role_repo.get_by_id(shift_data.required_role_id)
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Role with id {shift_data.required_role_id} not found"
                )
        
        # Create shift
        shift = Shift(**shift_data.model_dump())
        created_shift = self.shift_repo.create(shift)
        
        return ShiftResponse.model_validate(created_shift)

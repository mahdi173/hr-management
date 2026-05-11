"""Update Shift Use Case - Business logic for updating shifts"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..shared.shift_dto import ShiftUpdate, ShiftResponse
from ....repositories.shift_repository import ShiftRepository
from ....repositories.role_repository import RoleRepository


class UpdateShiftUseCase:
    """Use case for updating an existing shift"""
    
    def __init__(self, db: Session):
        self.db = db
        self.shift_repo = ShiftRepository(db)
        self.role_repo = RoleRepository(db)
    
    def execute(self, shift_id: int, shift_data: ShiftUpdate) -> ShiftResponse:
        """
        Update an existing shift
        
        Business rules:
        - Shift must exist
        - Required role must exist (if provided and changed)
        - Time validation (start < end)
        - Employee limits validation (max >= min)
        """
        # Get existing shift
        shift = self.shift_repo.get_by_id(shift_id)
        if not shift:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shift with id {shift_id} not found"
            )
        
        # Validate required role exists (if being updated)
        if shift_data.required_role_id is not None:
            role = self.role_repo.get_by_id(shift_data.required_role_id)
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Role with id {shift_data.required_role_id} not found"
                )
        
        # Get update data (exclude unset fields)
        update_data = shift_data.model_dump(exclude_unset=True)
        
        # Validate time order if both times are being updated
        if 'start_time' in update_data and 'end_time' in update_data:
            if update_data['start_time'] >= update_data['end_time']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="end_time must be after start_time"
                )
        # Validate time order if only start_time is being updated
        elif 'start_time' in update_data:
            if update_data['start_time'] >= shift.end_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="start_time must be before current end_time"
                )
        # Validate time order if only end_time is being updated
        elif 'end_time' in update_data:
            if shift.start_time >= update_data['end_time']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="end_time must be after current start_time"
                )
        
        # Validate employee limits if being updated
        min_emp = update_data.get('min_employees', shift.min_employees)
        max_emp = update_data.get('max_employees', shift.max_employees)
        if max_emp < min_emp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="max_employees must be greater than or equal to min_employees"
            )
        
        # Update shift
        updated_shift = self.shift_repo.update(shift_id, update_data)
        
        return ShiftResponse.model_validate(updated_shift)

"""Update Shift Controller - API endpoint for updating shifts"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..shared.shift_dto import ShiftUpdate, ShiftResponse
from .update_shift_usecase import UpdateShiftUseCase
from ....database import get_db


router = APIRouter()


@router.put(
    "/shifts/{shift_id}",
    response_model=ShiftResponse,
    summary="Update a shift",
    tags=["shifts"]
)
def update_shift(
    shift_id: int,
    shift_data: ShiftUpdate,
    db: Session = Depends(get_db)
) -> ShiftResponse:
    """
    Update an existing shift.
    
    - **shift_id**: ID of the shift to update
    - **shift_data**: Fields to update (all optional)
    
    Only provided fields will be updated. Other fields remain unchanged.
    """
    use_case = UpdateShiftUseCase(db)
    return use_case.execute(shift_id, shift_data)

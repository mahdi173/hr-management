"""Create Shift Controller - API endpoint for creating shifts"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..shared.shift_dto import ShiftCreate, ShiftResponse
from .create_shift_usecase import CreateShiftUseCase
from ....database import get_db


router = APIRouter()


@router.post(
    "/schedules/{schedule_id}/shifts",
    response_model=ShiftResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new shift",
    tags=["shifts"]
)
def create_shift(
    schedule_id: int,
    shift_data: ShiftCreate,
    db: Session = Depends(get_db)
) -> ShiftResponse:
    """
    Create a new shift for a schedule.
    
    - **schedule_id**: ID of the schedule to add the shift to
    - **shift_data**: Shift details including date, time, and staffing requirements
    
    Returns the created shift with all details.
    """
    # Ensure schedule_id from path matches the one in the request body
    if shift_data.schedule_id != schedule_id:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Schedule ID in path does not match schedule_id in request body"
        )
    
    use_case = CreateShiftUseCase(db)
    return use_case.execute(shift_data)

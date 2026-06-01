"""Get My Shifts Controller - GET /api/v1/shifts/me"""

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ....core.dependencies import get_current_user
from ....database import get_db
from ....models.user import User
from ..get_shifts.get_shifts_usecase import GetShiftsUseCase
from ..shared.shift_dto import ShiftResponse

router = APIRouter()


@router.get(
    "/shifts/me",
    response_model=List[ShiftResponse],
    summary="Get shifts for the current user",
    tags=["shifts"],
)
def get_my_shifts(
    start_date: Optional[date] = Query(None, description="Filter by start date"),
    end_date: Optional[date] = Query(None, description="Filter by end date"),
    include_assignments: bool = Query(True, description="Include shift assignments"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[ShiftResponse]:
    if not current_user.employee_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not linked to an employee profile",
        )

    use_case = GetShiftsUseCase(db)
    return use_case.execute(
        start_date=start_date,
        end_date=end_date,
        employee_id=current_user.employee_id,
        skip=skip,
        limit=limit,
        include_assignments=include_assignments,
    )

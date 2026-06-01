"""Get My Hours Controller - GET /api/v1/shifts/me/hours"""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ....core.dependencies import get_current_user
from ....database import get_db
from ....models.user import User
from ..get_hours.get_hours_usecase import GetHoursUseCase
from ..shared.shift_dto import HoursSummary

router = APIRouter()


@router.get(
    "/shifts/me/hours",
    response_model=HoursSummary,
    summary="Get working hours summary for the current user",
    tags=["shifts"],
)
def get_my_hours(
    start_date: date = Query(..., description="Start date of the period"),
    end_date: date = Query(..., description="End date of the period"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> HoursSummary:
    if not current_user.employee_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not linked to an employee profile",
        )

    use_case = GetHoursUseCase(db)
    return use_case.execute(current_user.employee_id, start_date, end_date)

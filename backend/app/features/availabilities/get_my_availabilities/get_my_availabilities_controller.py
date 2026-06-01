"""Get My Availabilities Controller - GET /availabilities/me"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ....core.dependencies import get_current_user
from ....database import get_db
from ....models.user import User
from ..get_employee_availabilities.get_employee_availabilities_usecase import (
    GetEmployeeAvailabilitiesUseCase,
)
from ..shared.availability_dto import AvailabilityResponse

router = APIRouter()


@router.get(
    "/availabilities/me",
    response_model=List[AvailabilityResponse],
    summary="Get availabilities for the current user",
)
def get_my_availabilities(
    active_only: bool = Query(True, description="Return only active availabilities"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.employee_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not linked to an employee profile",
        )

    use_case = GetEmployeeAvailabilitiesUseCase(db)
    return use_case.execute(current_user.employee_id, active_only=active_only)

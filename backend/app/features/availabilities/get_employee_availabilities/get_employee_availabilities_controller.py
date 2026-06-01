"""Get Employee Availabilities Controller - HTTP endpoint for listing employee availabilities"""

from typing import List

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from ....core.authorization import verify_resource_access
from ....core.dependencies import get_current_user
from ....database import get_db
from ....models.user import User
from ..shared.availability_dto import AvailabilityResponse
from .get_employee_availabilities_usecase import GetEmployeeAvailabilitiesUseCase

router = APIRouter()


@router.get(
    "/employees/{employee_id}/availabilities",
    response_model=List[AvailabilityResponse],
    summary="Get all availabilities for an employee",
)
def get_employee_availabilities(
    employee_id: int = Path(..., gt=0, description="The ID of the employee"),
    active_only: bool = Query(True, description="Filter to show only active availabilities"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_resource_access(current_user, employee_id)
    use_case = GetEmployeeAvailabilitiesUseCase(db)
    return use_case.execute(employee_id, active_only=active_only)

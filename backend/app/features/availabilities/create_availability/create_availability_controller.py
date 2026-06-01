"""Create Availability Controller - HTTP endpoint for creating availabilities"""

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from ....core.authorization import verify_resource_access
from ....core.dependencies import get_current_user
from ....database import get_db
from ....models.user import User
from ..shared.availability_dto import AvailabilityCreate, AvailabilityResponse
from .create_availability_usecase import CreateAvailabilityUseCase

router = APIRouter()


@router.post(
    "/employees/{employee_id}/availabilities",
    response_model=AvailabilityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new availability for an employee",
)
def create_availability(
    employee_id: int = Path(..., gt=0, description="The ID of the employee"),
    availability_data: AvailabilityCreate = ...,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if availability_data.employee_id != employee_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="employee_id in path must match employee_id in request body",
        )
    verify_resource_access(current_user, employee_id)
    use_case = CreateAvailabilityUseCase(db)
    return use_case.execute(availability_data)

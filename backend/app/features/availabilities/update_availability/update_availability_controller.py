"""Update Availability Controller - HTTP endpoint for updating availabilities"""

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from ....core.authorization import verify_availability_access
from ....core.dependencies import get_current_user
from ....database import get_db
from ....models.user import User
from ..shared.availability_dto import AvailabilityUpdate, AvailabilityResponse
from .update_availability_usecase import UpdateAvailabilityUseCase

router = APIRouter()


@router.put(
    "/availabilities/{availability_id}",
    response_model=AvailabilityResponse,
    summary="Update an availability",
)
def update_availability(
    availability_data: AvailabilityUpdate,
    availability_id: int = Path(..., gt=0, description="The ID of the availability"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_availability_access(current_user, db, availability_id)
    use_case = UpdateAvailabilityUseCase(db)
    return use_case.execute(availability_id, availability_data)

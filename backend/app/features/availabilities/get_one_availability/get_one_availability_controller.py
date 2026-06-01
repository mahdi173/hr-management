"""Get One Availability Controller - HTTP endpoint for retrieving a single availability"""

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from ....core.authorization import verify_availability_access
from ....core.dependencies import get_current_user
from ....database import get_db
from ....models.user import User
from ..shared.availability_dto import AvailabilityResponse
from .get_one_availability_usecase import GetOneAvailabilityUseCase

router = APIRouter()


@router.get(
    "/availabilities/{availability_id}",
    response_model=AvailabilityResponse,
    summary="Get an availability by ID",
)
def get_one_availability(
    availability_id: int = Path(..., gt=0, description="The ID of the availability"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_availability_access(current_user, db, availability_id)
    use_case = GetOneAvailabilityUseCase(db)
    return use_case.execute(availability_id)

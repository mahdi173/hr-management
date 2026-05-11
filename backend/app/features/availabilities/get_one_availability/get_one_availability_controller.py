"""Get One Availability Controller - HTTP endpoint for retrieving a single availability"""

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared.availability_dto import AvailabilityResponse
from .get_one_availability_usecase import GetOneAvailabilityUseCase

router = APIRouter()


@router.get(
    "/availabilities/{availability_id}",
    response_model=AvailabilityResponse,
    summary="Get an availability by ID",
    description="Retrieve a specific availability by its unique identifier.",
    responses={
        200: {"description": "Availability retrieved successfully"},
        404: {"description": "Availability not found"},
    }
)
def get_one_availability(
    availability_id: int = Path(..., gt=0, description="The ID of the availability to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Get a specific availability by ID
    
    - **availability_id**: Unique identifier of the availability
    """
    use_case = GetOneAvailabilityUseCase(db)
    return use_case.execute(availability_id)

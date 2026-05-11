"""Update Availability Controller - HTTP endpoint for updating availabilities"""

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared.availability_dto import AvailabilityUpdate, AvailabilityResponse
from .update_availability_usecase import UpdateAvailabilityUseCase

router = APIRouter()


@router.put(
    "/availabilities/{availability_id}",
    response_model=AvailabilityResponse,
    summary="Update an availability",
    description="Update an existing availability. Only modifiable fields: start_time, end_time, is_active.",
    responses={
        200: {"description": "Availability updated successfully"},
        404: {"description": "Availability not found"},
        400: {"description": "Updated availability overlaps with existing availability"},
    }
)
def update_availability(
    availability_data: AvailabilityUpdate,
    availability_id: int = Path(..., gt=0, description="The ID of the availability to update"),
    db: Session = Depends(get_db)
):
    """
    Update an existing availability
    
    - **availability_id**: Unique identifier of the availability to update
    - **start_time**: Optional new start time
    - **end_time**: Optional new end time
    - **is_active**: Optional new active status
    
    Note: Cannot change employee_id, day_of_week, is_recurring, or specific_date
    """
    use_case = UpdateAvailabilityUseCase(db)
    return use_case.execute(availability_id, availability_data)

"""Create Availability Controller - HTTP endpoint for creating availabilities"""

from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared.availability_dto import AvailabilityCreate, AvailabilityResponse
from .create_availability_usecase import CreateAvailabilityUseCase

router = APIRouter()


@router.post(
    "/employees/{employee_id}/availabilities",
    response_model=AvailabilityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new availability for an employee",
    description="Create a new availability slot for an employee. Can be recurring (weekly) or for a specific date.",
    responses={
        201: {"description": "Availability created successfully"},
        400: {"description": "Availability overlaps with existing availability"},
        404: {"description": "Employee not found"},
    }
)
def create_availability(
    employee_id: int = Path(..., gt=0, description="The ID of the employee"),
    availability_data: AvailabilityCreate = ...,
    db: Session = Depends(get_db)
):
    """
    Create a new availability for an employee
    
    - **employee_id**: ID of the employee (must match availability_data.employee_id)
    - **start_time**: Start time of availability (HH:MM:SS format)
    - **end_time**: End time of availability (HH:MM:SS format)
    - **is_recurring**: True for weekly recurring, False for specific date
    - **day_of_week**: 0-6 (Monday-Sunday) - required if is_recurring=True
    - **specific_date**: YYYY-MM-DD - required if is_recurring=False
    - **is_active**: Whether the availability is active (default: true)
    """
    # Ensure employee_id in path matches employee_id in body
    if availability_data.employee_id != employee_id:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="employee_id in path must match employee_id in request body"
        )
    
    use_case = CreateAvailabilityUseCase(db)
    return use_case.execute(availability_data)

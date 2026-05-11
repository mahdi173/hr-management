"""Get Employee Availabilities Controller - HTTP endpoint for listing employee availabilities"""

from typing import List
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared.availability_dto import AvailabilityResponse
from .get_employee_availabilities_usecase import GetEmployeeAvailabilitiesUseCase

router = APIRouter()


@router.get(
    "/employees/{employee_id}/availabilities",
    response_model=List[AvailabilityResponse],
    summary="Get all availabilities for an employee",
    description="Retrieve all availability slots for a specific employee with optional filtering.",
    responses={
        200: {"description": "List of availabilities retrieved successfully"},
        404: {"description": "Employee not found"},
    }
)
def get_employee_availabilities(
    employee_id: int = Path(..., gt=0, description="The ID of the employee"),
    active_only: bool = Query(True, description="Filter to show only active availabilities"),
    db: Session = Depends(get_db)
):
    """
    Get all availabilities for an employee
    
    - **employee_id**: ID of the employee
    - **active_only**: If true, returns only active availabilities (default: true)
    """
    use_case = GetEmployeeAvailabilitiesUseCase(db)
    return use_case.execute(employee_id, active_only=active_only)

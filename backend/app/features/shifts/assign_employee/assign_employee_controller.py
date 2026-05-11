"""Assign Employee Controller - API endpoint for assigning employees to shifts"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..shared.shift_dto import ShiftAssignmentCreate, ShiftAssignmentResponse
from .assign_employee_usecase import AssignEmployeeUseCase
from ....database import get_db


router = APIRouter()


@router.post(
    "/shifts/{shift_id}/assign",
    response_model=ShiftAssignmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Assign employee to shift",
    tags=["shifts"]
)
def assign_employee(
    shift_id: int,
    assignment_data: ShiftAssignmentCreate,
    db: Session = Depends(get_db)
) -> ShiftAssignmentResponse:
    """
    Assign an employee to a shift.
    
    - **shift_id**: ID of the shift to assign employee to
    - **assignment_data**: Assignment details including employee_id
    
    Validates:
    - Employee availability during shift time
    - No overlapping shift assignments
    - No approved absences
    - Shift capacity not exceeded
    
    Returns the created assignment.
    """
    # Ensure shift_id from path matches the one in the request body
    if assignment_data.shift_id != shift_id:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Shift ID in path does not match shift_id in request body"
        )
    
    use_case = AssignEmployeeUseCase(db)
    return use_case.execute(assignment_data)

"""Remove Assignment Controller - API endpoint for removing employee from shift"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .remove_assignment_usecase import RemoveAssignmentUseCase
from ....core.dependencies import require_manager
from ....database import get_db
from ....models.user import User


router = APIRouter()


@router.delete(
    "/shifts/{shift_id}/assign/{employee_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove employee from shift",
    tags=["shifts"]
)
def remove_assignment(
    shift_id: int,
    employee_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_manager)
) -> dict:
    """
    Remove an employee assignment from a shift.
    
    - **shift_id**: ID of the shift
    - **employee_id**: ID of the employee to remove
    
    Validates:
    - Assignment exists
    - Removing doesn't violate minimum staffing requirements
    
    Returns a confirmation message.
    """
    use_case = RemoveAssignmentUseCase(db)
    return use_case.execute(shift_id, employee_id)

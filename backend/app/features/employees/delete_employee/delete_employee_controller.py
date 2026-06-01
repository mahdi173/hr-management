"""Delete Employee Controller - HTTP endpoint for deleting employees"""

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from ....core.dependencies import require_admin
from ....database import get_db
from ....models.user import User
from .delete_employee_usecase import DeleteEmployeeUseCase

router = APIRouter()


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete employee",
    description="Delete an employee (soft delete by default)"
)
def delete_employee(
    id: int,
    hard_delete: bool = Query(False, description="Permanently delete if true, soft delete if false"),
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    """
    Delete an employee:
    
    - **id**: The unique identifier of the employee
    - **hard_delete**: If true, permanently delete; if false, soft delete (default: false)
    """
    use_case = DeleteEmployeeUseCase(db)
    use_case.execute(id, hard_delete=hard_delete)
    return None

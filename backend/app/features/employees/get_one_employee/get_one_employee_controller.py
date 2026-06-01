"""Get One Employee Controller - HTTP endpoint for retrieving a single employee"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....core.authorization import verify_resource_access
from ....core.dependencies import get_current_user
from ....database import get_db
from ....models.user import User
from ..shared import EmployeeResponse
from .get_one_employee_usecase import GetOneEmployeeUseCase

router = APIRouter()


@router.get(
    "/{id}",
    response_model=EmployeeResponse,
    summary="Get employee by ID",
    description="Retrieve a specific employee by their ID"
)
def get_one_employee(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get an employee by their ID:
    
    - **id**: The unique identifier of the employee
    """
    verify_resource_access(current_user, id)
    use_case = GetOneEmployeeUseCase(db)
    return use_case.execute(id)

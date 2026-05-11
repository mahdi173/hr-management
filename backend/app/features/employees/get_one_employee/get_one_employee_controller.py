"""Get One Employee Controller - HTTP endpoint for retrieving a single employee"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....database import get_db
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
    db: Session = Depends(get_db)
):
    """
    Get an employee by their ID:
    
    - **id**: The unique identifier of the employee
    """
    use_case = GetOneEmployeeUseCase(db)
    return use_case.execute(id)

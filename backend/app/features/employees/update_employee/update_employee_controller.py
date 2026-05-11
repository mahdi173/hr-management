"""Update Employee Controller - HTTP endpoint for updating employees"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared import EmployeeUpdate, EmployeeResponse
from .update_employee_usecase import UpdateEmployeeUseCase

router = APIRouter()


@router.put(
    "/{id}",
    response_model=EmployeeResponse,
    summary="Update employee",
    description="Update an existing employee's information"
)
def update_employee(
    id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an employee's information:
    
    - **id**: The unique identifier of the employee
    - All fields are optional - only provided fields will be updated
    """
    use_case = UpdateEmployeeUseCase(db)
    return use_case.execute(id, employee)

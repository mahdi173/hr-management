"""Create Employee Controller - HTTP endpoint for creating employees"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared import EmployeeCreate, EmployeeResponse
from .create_employee_usecase import CreateEmployeeUseCase

router = APIRouter()


@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee",
    description="Create a new employee with the provided information"
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new employee with all the information:
    
    - **first_name**: Employee's first name (required)
    - **last_name**: Employee's last name (required)
    - **email**: Unique email address (required)
    - **phone**: Phone number (optional)
    - **role_id**: ID of the employee's role (optional)
    - **contract_type_id**: ID of the contract type (optional)
    - **is_active**: Whether the employee is active (default: True)
    """
    use_case = CreateEmployeeUseCase(db)
    return use_case.execute(employee)

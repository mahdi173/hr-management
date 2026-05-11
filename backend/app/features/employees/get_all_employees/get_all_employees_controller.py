"""Get All Employees Controller - HTTP endpoint for listing employees"""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared import EmployeeResponse
from .get_all_employees_usecase import GetAllEmployeesUseCase

router = APIRouter()


@router.get(
    "/",
    response_model=List[EmployeeResponse],
    summary="List all employees",
    description="Retrieve a list of employees with pagination and filtering options"
)
def get_all_employees(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    active_only: bool = Query(False, description="Filter for active employees only"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of employees with pagination:
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 1000)
    - **active_only**: If true, only return active employees (default: false)
    """
    use_case = GetAllEmployeesUseCase(db)
    return use_case.execute(skip=skip, limit=limit, active_only=active_only)

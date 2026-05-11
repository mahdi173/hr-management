"""Get Employees By Role Controller - HTTP endpoint for filtering employees by role"""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared import EmployeeResponse
from .get_employees_by_role_usecase import GetEmployeesByRoleUseCase

router = APIRouter()


@router.get(
    "/role/{role_id}",
    response_model=List[EmployeeResponse],
    summary="Get employees by role",
    description="Retrieve all employees with a specific role"
)
def get_employees_by_role(
    role_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get employees by role ID:
    
    - **role_id**: The ID of the role
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 1000)
    """
    use_case = GetEmployeesByRoleUseCase(db)
    return use_case.execute(role_id, skip=skip, limit=limit)

"""Create Role Controller - HTTP endpoints for creating roles"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared.role_dto import RoleCreate, RoleResponse
from .create_role_usecase import CreateRoleUseCase

router = APIRouter()


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(role_data: RoleCreate, db: Session = Depends(get_db)):
    """
    Create a new role
    
    Args:
        role_data: Role creation data
        db: Database session
        
    Returns:
        Created role instance
    """
    use_case = CreateRoleUseCase(db)
    return use_case.execute(role_data)

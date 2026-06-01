"""Get All Roles Controller - HTTP endpoints for listing roles"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....core.dependencies import get_current_user
from ....database import get_db
from ....models.user import User
from ..shared.role_dto import RoleResponse
from .get_all_roles_usecase import GetAllRolesUseCase

router = APIRouter()


@router.get("/", response_model=List[RoleResponse])
def get_all_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user)):
    """
    Get all roles with pagination
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of roles
    """
    use_case = GetAllRolesUseCase(db)
    return use_case.execute(skip=skip, limit=limit)

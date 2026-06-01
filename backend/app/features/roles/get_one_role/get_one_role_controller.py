"""Get One Role Controller - HTTP endpoints for getting a single role"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....core.dependencies import get_current_user
from ....database import get_db
from ....models.user import User
from ..shared.role_dto import RoleResponse
from .get_one_role_usecase import GetOneRoleUseCase

router = APIRouter()


@router.get("/{role_id}", response_model=RoleResponse)
def get_one_role(role_id: int, db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user)):
    """
    Get a single role by ID
    
    Args:
        role_id: ID of the role to retrieve
        db: Database session
        
    Returns:
        Role instance
    """
    use_case = GetOneRoleUseCase(db)
    return use_case.execute(role_id)

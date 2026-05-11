"""Update Role Controller - HTTP endpoints for updating roles"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared.role_dto import RoleUpdate, RoleResponse
from .update_role_usecase import UpdateRoleUseCase

router = APIRouter()


@router.put("/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role_data: RoleUpdate, db: Session = Depends(get_db)):
    """
    Update an existing role
    
    Args:
        role_id: ID of the role to update
        role_data: Role update data
        db: Database session
        
    Returns:
        Updated role instance
    """
    use_case = UpdateRoleUseCase(db)
    return use_case.execute(role_id, role_data)

"""Create Role Use Case - Business logic for creating roles"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.role_repository import RoleRepository
from ..shared.role_dto import RoleCreate
from ....models.role import Role


class CreateRoleUseCase:
    """Use case for creating a new role"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = RoleRepository(db)

    def execute(self, role_data: RoleCreate) -> Role:
        """
        Execute the create role use case
        
        Args:
            role_data: Role creation data
            
        Returns:
            Created role instance
            
        Raises:
            HTTPException: If role name already exists
        """
        # Check if name already exists
        if self.repository.name_exists(role_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role with name '{role_data.name}' already exists"
            )

        # Create role
        role_dict = role_data.model_dump()
        return self.repository.create(role_dict)

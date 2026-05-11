"""Update Role Use Case - Business logic for updating roles"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.role_repository import RoleRepository
from ..shared.role_dto import RoleUpdate
from ....models.role import Role


class UpdateRoleUseCase:
    """Use case for updating an existing role"""

    def __init__(self, db: Session):
        self.repository = RoleRepository(db)

    def execute(self, role_id: int, role_data: RoleUpdate) -> Role:
        """
        Execute the update role use case
        
        Args:
            role_id: ID of the role to update
            role_data: Role update data
            
        Returns:
            Updated role instance
            
        Raises:
            HTTPException: If role is not found or new name already exists
        """
        # Check if role exists
        if not self.repository.exists(role_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id {role_id} not found"
            )

        # If name is being updated, check if it already exists
        if role_data.name and self.repository.name_exists(role_data.name, exclude_id=role_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role with name '{role_data.name}' already exists"
            )

        # Update role
        update_data = role_data.model_dump(exclude_unset=True)
        return self.repository.update(role_id, update_data)

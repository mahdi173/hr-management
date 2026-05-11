"""Get One Role Use Case - Business logic for getting a single role"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.role_repository import RoleRepository
from ....models.role import Role


class GetOneRoleUseCase:
    """Use case for getting a single role by ID"""

    def __init__(self, db: Session):
        self.repository = RoleRepository(db)

    def execute(self, role_id: int) -> Role:
        """
        Execute the get one role use case
        
        Args:
            role_id: ID of the role to retrieve
            
        Returns:
            Role instance
            
        Raises:
            HTTPException: If role is not found
        """
        role = self.repository.get_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id {role_id} not found"
            )
        return role

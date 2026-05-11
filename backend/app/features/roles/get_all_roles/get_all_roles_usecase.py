"""Get All Roles Use Case - Business logic for listing roles"""

from typing import List
from sqlalchemy.orm import Session

from ....repositories.role_repository import RoleRepository
from ....models.role import Role


class GetAllRolesUseCase:
    """Use case for listing all roles"""

    def __init__(self, db: Session):
        self.repository = RoleRepository(db)

    def execute(self, skip: int = 0, limit: int = 100) -> List[Role]:
        """
        Execute the get all roles use case
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of role instances
        """
        return self.repository.get_all(skip=skip, limit=limit)

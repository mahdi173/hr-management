"""Get Employees By Role Use Case - Business logic for filtering employees by role"""

from typing import List
from sqlalchemy.orm import Session

from ....repositories.employee_repository import EmployeeRepository
from ....models.employee import Employee


class GetEmployeesByRoleUseCase:
    """Use case for retrieving employees by role"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = EmployeeRepository(db)

    def execute(self, role_id: int, skip: int = 0, limit: int = 100) -> List[Employee]:
        """
        Execute the get employees by role use case
        
        Args:
            role_id: Role ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of employee instances
        """
        return self.repository.get_by_role(role_id, skip=skip, limit=limit)

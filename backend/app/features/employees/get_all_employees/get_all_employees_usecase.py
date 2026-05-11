"""Get All Employees Use Case - Business logic for listing employees"""

from typing import List
from sqlalchemy.orm import Session

from ....repositories.employee_repository import EmployeeRepository
from ....models.employee import Employee


class GetAllEmployeesUseCase:
    """Use case for retrieving all employees with pagination and filtering"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = EmployeeRepository(db)

    def execute(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        active_only: bool = False
    ) -> List[Employee]:
        """
        Execute the get all employees use case
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            active_only: If True, only return active employees
            
        Returns:
            List of employee instances
        """
        if active_only:
            return self.repository.get_active_employees(skip=skip, limit=limit)
        return self.repository.get_all(skip=skip, limit=limit)

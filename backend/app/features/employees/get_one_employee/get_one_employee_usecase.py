"""Get One Employee Use Case - Business logic for retrieving a single employee"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.employee_repository import EmployeeRepository
from ....models.employee import Employee


class GetOneEmployeeUseCase:
    """Use case for retrieving a single employee by ID"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = EmployeeRepository(db)

    def execute(self, employee_id: int) -> Employee:
        """
        Execute the get one employee use case
        
        Args:
            employee_id: Employee ID
            
        Returns:
            Employee instance
            
        Raises:
            HTTPException: If employee not found
        """
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with id {employee_id} not found"
            )
        return employee

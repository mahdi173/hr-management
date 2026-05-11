"""Delete Employee Use Case - Business logic for deleting employees"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.employee_repository import EmployeeRepository


class DeleteEmployeeUseCase:
    """Use case for deleting an employee (soft delete by default)"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = EmployeeRepository(db)

    def execute(self, employee_id: int, hard_delete: bool = False) -> bool:
        """
        Execute the delete employee use case
        
        Args:
            employee_id: Employee ID
            hard_delete: If True, permanently delete; if False, soft delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            HTTPException: If employee not found
        """
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with id {employee_id} not found"
            )

        if hard_delete:
            return self.repository.delete(employee_id)
        else:
            self.repository.soft_delete(employee_id)
            return True

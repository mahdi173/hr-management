"""Get Employee Availabilities Use Case - Business logic for retrieving employee availabilities"""

from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.availability_repository import AvailabilityRepository
from ....repositories.employee_repository import EmployeeRepository
from ....models.availability import Availability


class GetEmployeeAvailabilitiesUseCase:
    """Use case for retrieving all availabilities for an employee"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = AvailabilityRepository(db)
        self.employee_repository = EmployeeRepository(db)

    def execute(self, employee_id: int, active_only: bool = True) -> List[Availability]:
        """
        Execute the get employee availabilities use case
        
        Args:
            employee_id: ID of the employee
            active_only: If True, return only active availabilities
            
        Returns:
            List of availability instances
            
        Raises:
            HTTPException: If employee doesn't exist
        """
        # Check if employee exists
        employee = self.employee_repository.get_by_id(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with id {employee_id} not found"
            )

        return self.repository.get_by_employee(employee_id, active_only=active_only)

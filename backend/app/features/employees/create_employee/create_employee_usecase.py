"""Create Employee Use Case - Business logic for creating employees"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.employee_repository import EmployeeRepository
from ..shared import EmployeeCreate
from ....models.employee import Employee
from ....models.role import Role
from ....models.contract_type import ContractType


class CreateEmployeeUseCase:
    """Use case for creating a new employee"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = EmployeeRepository(db)

    def execute(self, employee_data: EmployeeCreate) -> Employee:
        """
        Execute the create employee use case
        
        Args:
            employee_data: Employee creation data
            
        Returns:
            Created employee instance
            
        Raises:
            HTTPException: If email already exists or role/contract_type doesn't exist
        """
        # Check if email already exists
        if self.repository.email_exists(employee_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {employee_data.email} already exists"
            )

        # Validate role exists if provided
        if employee_data.role_id:
            role = self.db.query(Role).filter(Role.id == employee_data.role_id).first()
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Role with id {employee_data.role_id} not found"
                )

        # Validate contract type exists if provided
        if employee_data.contract_type_id:
            contract_type = self.db.query(ContractType).filter(
                ContractType.id == employee_data.contract_type_id
            ).first()
            if not contract_type:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Contract type with id {employee_data.contract_type_id} not found"
                )

        # Create employee
        employee_dict = employee_data.model_dump()
        return self.repository.create(employee_dict)

"""Update Employee Use Case - Business logic for updating employees"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.employee_repository import EmployeeRepository
from ..shared import EmployeeUpdate
from ....models.employee import Employee
from ....models.role import Role
from ....models.contract_type import ContractType


class UpdateEmployeeUseCase:
    """Use case for updating an existing employee"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = EmployeeRepository(db)

    def execute(self, employee_id: int, employee_data: EmployeeUpdate) -> Employee:
        """
        Execute the update employee use case
        
        Args:
            employee_id: Employee ID
            employee_data: Employee update data
            
        Returns:
            Updated employee instance
            
        Raises:
            HTTPException: If employee not found, email exists, or role/contract_type doesn't exist
        """
        # Check if employee exists
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with id {employee_id} not found"
            )

        # Get update data (exclude unset fields)
        update_data = employee_data.model_dump(exclude_unset=True)

        # Check email uniqueness if email is being updated
        if "email" in update_data:
            if self.repository.email_exists(update_data["email"], exclude_id=employee_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email {update_data['email']} already exists"
                )

        # Validate role exists if being updated
        if "role_id" in update_data and update_data["role_id"]:
            role = self.db.query(Role).filter(Role.id == update_data["role_id"]).first()
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Role with id {update_data['role_id']} not found"
                )

        # Validate contract type exists if being updated
        if "contract_type_id" in update_data and update_data["contract_type_id"]:
            contract_type = self.db.query(ContractType).filter(
                ContractType.id == update_data["contract_type_id"]
            ).first()
            if not contract_type:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Contract type with id {update_data['contract_type_id']} not found"
                )

        # Update employee
        return self.repository.update(employee_id, update_data)

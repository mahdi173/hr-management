"""Create Contract Type Use Case - Business logic for creating contract types"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.contract_type_repository import ContractTypeRepository
from ..shared.contract_type_dto import ContractTypeCreate
from ....models.contract_type import ContractType


class CreateContractTypeUseCase:
    """Use case for creating a new contract type"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = ContractTypeRepository(db)

    def execute(self, contract_type_data: ContractTypeCreate) -> ContractType:
        """
        Execute the create contract type use case
        
        Args:
            contract_type_data: Contract type creation data
            
        Returns:
            Created contract type instance
            
        Raises:
            HTTPException: If contract type name already exists
        """
        # Check if name already exists
        if self.repository.name_exists(contract_type_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Contract type with name '{contract_type_data.name}' already exists"
            )

        # Validate max_weekly_hours is greater than weekly_hours if provided
        if contract_type_data.max_weekly_hours is not None:
            if contract_type_data.max_weekly_hours < contract_type_data.weekly_hours:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="max_weekly_hours must be greater than or equal to weekly_hours"
                )

        # Create contract type
        contract_type_dict = contract_type_data.model_dump()
        return self.repository.create(contract_type_dict)

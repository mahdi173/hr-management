"""Update Contract Type Use Case - Business logic for updating contract types"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.contract_type_repository import ContractTypeRepository
from ..shared.contract_type_dto import ContractTypeUpdate
from ....models.contract_type import ContractType


class UpdateContractTypeUseCase:
    """Use case for updating an existing contract type"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = ContractTypeRepository(db)

    def execute(self, contract_type_id: int, contract_type_data: ContractTypeUpdate) -> ContractType:
        """
        Execute the update contract type use case
        
        Args:
            contract_type_id: ID of the contract type to update
            contract_type_data: Updated contract type data
            
        Returns:
            Updated contract type instance
            
        Raises:
            HTTPException: If contract type is not found or validation fails
        """
        # Check if contract type exists
        contract_type = self.repository.get_by_id(contract_type_id)
        if not contract_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contract type with id {contract_type_id} not found"
            )

        # Check if new name already exists (if name is being updated)
        if contract_type_data.name is not None:
            if self.repository.name_exists(contract_type_data.name, exclude_id=contract_type_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Contract type with name '{contract_type_data.name}' already exists"
                )

        # Get the update data, excluding unset fields
        update_dict = contract_type_data.model_dump(exclude_unset=True)

        # Validate max_weekly_hours vs weekly_hours if either is being updated
        if update_dict:
            current_weekly_hours = contract_type.weekly_hours
            current_max_weekly_hours = contract_type.max_weekly_hours
            
            new_weekly_hours = update_dict.get('weekly_hours', current_weekly_hours)
            new_max_weekly_hours = update_dict.get('max_weekly_hours', current_max_weekly_hours)
            
            if new_max_weekly_hours is not None and new_max_weekly_hours < new_weekly_hours:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="max_weekly_hours must be greater than or equal to weekly_hours"
                )

        # Update contract type
        return self.repository.update(contract_type_id, update_dict)

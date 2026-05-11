"""Get One Contract Type Use Case - Business logic for retrieving a single contract type"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.contract_type_repository import ContractTypeRepository
from ....models.contract_type import ContractType


class GetOneContractTypeUseCase:
    """Use case for retrieving a single contract type by ID"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = ContractTypeRepository(db)

    def execute(self, contract_type_id: int) -> ContractType:
        """
        Execute the get one contract type use case
        
        Args:
            contract_type_id: ID of the contract type to retrieve
            
        Returns:
            Contract type instance
            
        Raises:
            HTTPException: If contract type is not found
        """
        contract_type = self.repository.get_by_id(contract_type_id)
        
        if not contract_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contract type with id {contract_type_id} not found"
            )
        
        return contract_type

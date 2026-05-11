"""Get All Contract Types Use Case - Business logic for listing contract types"""

from typing import List
from sqlalchemy.orm import Session

from ....repositories.contract_type_repository import ContractTypeRepository
from ....models.contract_type import ContractType


class GetAllContractTypesUseCase:
    """Use case for retrieving all contract types with optional filtering"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = ContractTypeRepository(db)

    def execute(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False
    ) -> List[ContractType]:
        """
        Execute the get all contract types use case
        
        Args:
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return
            active_only: If True, return only active contract types
            
        Returns:
            List of contract type instances
        """
        if active_only:
            return self.repository.get_active_contract_types(skip=skip, limit=limit)
        else:
            return self.repository.get_all(skip=skip, limit=limit)

"""
ContractType repository - handles data access for ContractType model.
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from ..models.contract_type import ContractType
from .base import BaseRepository


class ContractTypeRepository(BaseRepository[ContractType]):
    """Repository for ContractType model with custom queries"""

    def __init__(self, db: Session):
        """Initialize with ContractType model"""
        super().__init__(ContractType, db)

    def get_by_name(self, name: str) -> Optional[ContractType]:
        """
        Get contract type by name
        
        Args:
            name: Contract type name
            
        Returns:
            ContractType instance or None if not found
        """
        return self.db.query(self.model).filter(
            self.model.name == name
        ).first()

    def get_active_contract_types(self, skip: int = 0, limit: int = 100) -> List[ContractType]:
        """
        Get all active contract types with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of active contract type instances
        """
        return self.db.query(self.model).filter(
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def name_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if a contract type name already exists
        
        Args:
            name: Contract type name to check
            exclude_id: Optional contract type ID to exclude from check (for updates)
            
        Returns:
            True if name exists, False otherwise
        """
        query = self.db.query(self.model).filter(self.model.name == name)
        if exclude_id:
            query = query.filter(self.model.id != exclude_id)
        return query.first() is not None

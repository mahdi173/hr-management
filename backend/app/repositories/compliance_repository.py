"""Compliance repositories - handles data access for ComplianceRule and ComplianceViolation"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models.compliance import ComplianceRule, ComplianceViolation, RuleType
from .base import BaseRepository


class ComplianceRuleRepository(BaseRepository[ComplianceRule]):
    """Repository for ComplianceRule model"""
    
    def __init__(self, db: Session):
        super().__init__(ComplianceRule, db)
    
    def get_active_rules(self) -> List[ComplianceRule]:
        """Get all active compliance rules"""
        return self.db.query(ComplianceRule).filter(
            ComplianceRule.is_active == True
        ).all()
    
    def get_by_type(self, rule_type: RuleType) -> Optional[ComplianceRule]:
        """Get rule by type"""
        return self.db.query(ComplianceRule).filter(
            ComplianceRule.rule_type == rule_type
        ).first()


class ComplianceViolationRepository(BaseRepository[ComplianceViolation]):
    """Repository for ComplianceViolation model"""
    
    def __init__(self, db: Session):
        super().__init__(ComplianceViolation, db)
    
    def get_by_assignment(self, assignment_id: int) -> List[ComplianceViolation]:
        """Get violations for a specific assignment"""
        return self.db.query(ComplianceViolation).filter(
            ComplianceViolation.shift_assignment_id == assignment_id
        ).all()
    
    def get_unresolved(self) -> List[ComplianceViolation]:
        """Get all unresolved violations"""
        return self.db.query(ComplianceViolation).filter(
            ComplianceViolation.resolved == False
        ).all()

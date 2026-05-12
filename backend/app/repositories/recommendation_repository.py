"""Recommendation Repository - handles data access for AI recommendations"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.recommendation import AssignmentPreference
from ..models.shift import ShiftAssignment
from .base import BaseRepository


class RecommendationRepository(BaseRepository[AssignmentPreference]):
    """Repository for recommendation-related data"""
    
    def __init__(self, db: Session):
        super().__init__(AssignmentPreference, db)
    
    def get_preferences_by_employee(self, employee_id: int) -> List[AssignmentPreference]:
        """Get all preferences for an employee"""
        return self.db.query(AssignmentPreference).filter(
            AssignmentPreference.employee_id == employee_id
        ).all()
    
    def get_preference_score(self, employee_id: int, shift_type: str) -> float:
        """Get preference score for an employee and shift type"""
        pref = self.db.query(AssignmentPreference).filter(
            AssignmentPreference.employee_id == employee_id,
            AssignmentPreference.shift_type == shift_type
        ).first()
        return pref.preference_score if pref else 0.5
    
    def get_assignment_count_by_role(self, employee_id: int, role_id: int) -> int:
        """Count how many times an employee has been assigned to a specific role"""
        # This requires joining Shift and ShiftAssignment, but for now we simplify
        return self.db.query(ShiftAssignment).filter(
            ShiftAssignment.employee_id == employee_id
        ).count() # Placeholder for more complex role-based history

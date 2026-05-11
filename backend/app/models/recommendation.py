"""
Recommendation models - for AI-based assignment recommendations.
Phase 3 feature.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class AssignmentPreference(Base):
    """Assignment preference model - stores historical preference data for learning"""
    __tablename__ = "assignment_preferences"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Preference data
    shift_type = Column(String, nullable=False)  # e.g., "morning", "evening", "night"
    preference_score = Column(Float, default=0.5)  # 0.0 to 1.0, learned from successful assignments
    
    # Relationships
    employee = relationship("Employee")
    
    def __repr__(self):
        return f"<AssignmentPreference Employee:{self.employee_id} Type:{self.shift_type} Score:{self.preference_score}>"

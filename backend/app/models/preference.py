"""
Preference models - for learning employee preferences.
Phase 4 feature.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class EmployeePreference(Base):
    """Employee preference model - stores explicit and learned preferences"""
    __tablename__ = "employee_preferences"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Preference details
    preference_type = Column(String, nullable=False)  # e.g., "shift_time", "day_of_week", "colleague", "shift_type"
    preference_value = Column(JSON, nullable=False)  # Flexible storage for various preference types
    strength = Column(Float, default=0.5)  # 0.0 to 1.0, confidence in preference
    is_explicit = Column(Boolean, default=False)  # True if user-specified, False if learned
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    employee = relationship("Employee", back_populates="preferences")
    
    def __repr__(self):
        return f"<EmployeePreference Employee:{self.employee_id} Type:{self.preference_type} Strength:{self.strength}>"


class PreferredColleague(Base):
    """Preferred colleague model - tracks who works well together"""
    __tablename__ = "preferred_colleagues"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    preferred_colleague_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Preference strength (learned from co-assignments)
    strength = Column(Float, default=0.5)  # 0.0 to 1.0
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id], back_populates="preferred_by")
    preferred_colleague = relationship("Employee", foreign_keys=[preferred_colleague_id], back_populates="is_preferred_colleague")
    
    def __repr__(self):
        return f"<PreferredColleague Employee:{self.employee_id} PrefersWith:{self.preferred_colleague_id} Strength:{self.strength}>"

"""
Role model - represents job roles/positions.
Dev A owns this file.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class Role(Base):
    """Role/position model for employees"""
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    permissions = Column(JSON, nullable=True)  # Store permissions as JSON object
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    employees = relationship("Employee", back_populates="role")
    required_for_shifts = relationship("Shift", back_populates="required_role")
    
    def __repr__(self):
        return f"<Role {self.name}>"

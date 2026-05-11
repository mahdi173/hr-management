"""
ContractType model - represents employment contract types.
Dev A owns this file.
"""
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from .base import Base


class ContractType(Base):
    """Contract type model (CDI, CDD, Temps partiel, etc.)"""
    __tablename__ = "contract_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    weekly_hours = Column(Float, nullable=False)  # Default weekly hours (e.g., 35.0)
    max_weekly_hours = Column(Float, nullable=True)  # Maximum allowed weekly hours
    is_active = Column(Boolean, default=True)
    
    # Relationships
    employees = relationship("Employee", back_populates="contract_type")
    
    def __repr__(self):
        return f"<ContractType {self.name} ({self.weekly_hours}h/week)>"

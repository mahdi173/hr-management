"""
ScheduleTemplate model - for automatic schedule generation.
Phase 4 feature.
"""
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from .base import Base


class ScheduleTemplate(Base):
    """Schedule template model - defines recurring schedule patterns"""
    __tablename__ = "schedule_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=True)
    
    # Template data (stored as JSON)
    default_shifts = Column(JSON, nullable=False)  # Structure defining shift patterns
    rules = Column(JSON, nullable=True)  # Additional scheduling rules
    
    def __repr__(self):
        return f"<ScheduleTemplate {self.name}>"

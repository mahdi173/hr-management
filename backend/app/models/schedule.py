"""
Schedule model - represents work schedules.
Dev B owns this file.
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .base import Base


class ScheduleStatus(str, enum.Enum):
    """Schedule status"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Schedule(Base):
    """Schedule model for organizing shifts"""
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    # Date range
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Foreign keys
    created_by_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    
    # Status
    status = Column(Enum(ScheduleStatus), default=ScheduleStatus.DRAFT, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    created_by = relationship("Employee", back_populates="created_schedules")
    shifts = relationship("Shift", back_populates="schedule", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('start_date <= end_date', name='check_schedule_date_order'),
    )
    
    def __repr__(self):
        return f"<Schedule {self.name} ({self.start_date} to {self.end_date})>"

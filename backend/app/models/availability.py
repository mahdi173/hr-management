"""
Availability model - represents employee availability windows.
Dev A owns this file.
"""
from sqlalchemy import Column, Integer, Time, Date, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base


class Availability(Base):
    """Employee availability model"""
    __tablename__ = "availabilities"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Time information
    day_of_week = Column(Integer, nullable=True)  # 0-6 (Monday-Sunday), null for specific dates
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # Type flags
    is_recurring = Column(Boolean, default=True)  # True for weekly recurring, False for specific date
    specific_date = Column(Date, nullable=True)  # Used when is_recurring=False
    is_active = Column(Boolean, default=True)
    
    # Relationships
    employee = relationship("Employee", back_populates="availabilities")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('day_of_week IS NULL OR (day_of_week >= 0 AND day_of_week <= 6)', name='check_day_of_week'),
        CheckConstraint('start_time < end_time', name='check_time_order'),
    )
    
    def __repr__(self):
        if self.is_recurring:
            return f"<Availability Employee:{self.employee_id} Day:{self.day_of_week} {self.start_time}-{self.end_time}>"
        else:
            return f"<Availability Employee:{self.employee_id} Date:{self.specific_date} {self.start_time}-{self.end_time}>"

"""
Shift models - represents work shifts and employee assignments.
Dev B owns this file.
"""
from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey, Enum, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .base import Base


class ShiftAssignmentStatus(str, enum.Enum):
    """Shift assignment status"""
    ASSIGNED = "assigned"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"


class AssignmentType(str, enum.Enum):
    """Type of shift assignment"""
    REGULAR = "regular"
    OVERTIME = "overtime"


class Shift(Base):
    """Shift model - represents a work shift"""
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False, index=True)
    required_role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    
    # Time information
    date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # Staffing requirements
    min_employees = Column(Integer, default=1)
    max_employees = Column(Integer, default=1)
    
    # Additional info
    notes = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    schedule = relationship("Schedule", back_populates="shifts")
    required_role = relationship("Role", back_populates="required_for_shifts")
    assignments = relationship("ShiftAssignment", back_populates="shift", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="related_shift")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('start_time < end_time', name='check_shift_time_order'),
        CheckConstraint('min_employees > 0', name='check_min_employees_positive'),
        CheckConstraint('max_employees >= min_employees', name='check_max_gte_min_employees'),
    )
    
    def __repr__(self):
        return f"<Shift {self.date} {self.start_time}-{self.end_time}>"


class ShiftAssignment(Base):
    """Shift assignment model - links employees to shifts"""
    __tablename__ = "shift_assignments"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Assignment details
    status = Column(Enum(ShiftAssignmentStatus), default=ShiftAssignmentStatus.ASSIGNED, nullable=False)
    assignment_type = Column(Enum(AssignmentType), default=AssignmentType.REGULAR, nullable=False)
    is_overtime = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    shift = relationship("Shift", back_populates="assignments")
    employee = relationship("Employee", back_populates="shift_assignments")
    compliance_violations = relationship("ComplianceViolation", back_populates="shift_assignment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ShiftAssignment Shift:{self.shift_id} Employee:{self.employee_id} ({self.status.value})>"

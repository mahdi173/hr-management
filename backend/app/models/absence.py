"""
Absence models - represents employee absences and leave types.
Dev A owns this file.
"""
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .base import Base


class AbsenceStatus(str, enum.Enum):
    """Absence request status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class AbsenceType(Base):
    """Absence type model (vacation, sick leave, etc.)"""
    __tablename__ = "absence_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    requires_approval = Column(Boolean, default=True)
    is_paid = Column(Boolean, default=True)
    
    # Relationships
    absences = relationship("Absence", back_populates="absence_type")
    
    def __repr__(self):
        return f"<AbsenceType {self.name}>"


class Absence(Base):
    """Absence/leave request model"""
    __tablename__ = "absences"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    absence_type_id = Column(Integer, ForeignKey("absence_types.id"), nullable=False)
    approved_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    
    # Date range
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Details
    reason = Column(String, nullable=True)
    status = Column(Enum(AbsenceStatus), default=AbsenceStatus.PENDING, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id], back_populates="absences")
    absence_type = relationship("AbsenceType", back_populates="absences")
    approved_by = relationship("Employee", foreign_keys=[approved_by_id], back_populates="approved_absences")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('start_date <= end_date', name='check_absence_date_order'),
    )
    
    def __repr__(self):
        return f"<Absence Employee:{self.employee_id} {self.start_date} to {self.end_date} ({self.status.value})>"

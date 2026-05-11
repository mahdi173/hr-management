"""
Employee model - represents a team member.
Dev A owns this file.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class Employee(Base):
    """Employee/team member model"""
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    
    # Foreign keys
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    contract_type_id = Column(Integer, ForeignKey("contract_types.id"), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    role = relationship("Role", back_populates="employees")
    contract_type = relationship("ContractType", back_populates="employees")
    availabilities = relationship("Availability", back_populates="employee", cascade="all, delete-orphan")
    absences = relationship("Absence", foreign_keys="[Absence.employee_id]", back_populates="employee", cascade="all, delete-orphan")
    approved_absences = relationship("Absence", foreign_keys="[Absence.approved_by_id]", back_populates="approved_by")
    shift_assignments = relationship("ShiftAssignment", back_populates="employee", cascade="all, delete-orphan")
    created_schedules = relationship("Schedule", back_populates="created_by")
    user = relationship("User", back_populates="employee", uselist=False)
    preferences = relationship("EmployeePreference", back_populates="employee", cascade="all, delete-orphan")
    preferred_by = relationship("PreferredColleague", foreign_keys="[PreferredColleague.employee_id]", back_populates="employee", cascade="all, delete-orphan")
    is_preferred_colleague = relationship("PreferredColleague", foreign_keys="[PreferredColleague.preferred_colleague_id]", back_populates="preferred_colleague")
    
    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name} ({self.email})>"

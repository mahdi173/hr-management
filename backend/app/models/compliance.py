"""
Compliance models - represents rules and violations.
Phase 2 feature.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .base import Base


class RuleType(str, enum.Enum):
    """Type of compliance rule"""
    MAX_DAILY_HOURS = "max_daily_hours"
    MAX_WEEKLY_HOURS = "max_weekly_hours"
    MIN_REST_HOURS = "min_rest_hours"


class ViolationSeverity(str, enum.Enum):
    """Severity of compliance violation"""
    WARNING = "warning"
    ERROR = "error"


class ComplianceRule(Base):
    """Compliance rule model - defines scheduling rules"""
    __tablename__ = "compliance_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rule_type = Column(Enum(RuleType), nullable=False)
    threshold_value = Column(Float, nullable=False)  # e.g., 10.0 for 10 hours max
    is_blocking = Column(Boolean, default=False)  # If true, prevents saving; if false, just warns
    is_active = Column(Boolean, default=True)
    
    # Relationships
    violations = relationship("ComplianceViolation", back_populates="rule")
    
    def __repr__(self):
        return f"<ComplianceRule {self.name} ({self.rule_type.value}: {self.threshold_value})>"


class ComplianceViolation(Base):
    """Compliance violation model - tracks rule violations"""
    __tablename__ = "compliance_violations"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    shift_assignment_id = Column(Integer, ForeignKey("shift_assignments.id"), nullable=False, index=True)
    rule_id = Column(Integer, ForeignKey("compliance_rules.id"), nullable=False)
    
    # Violation details
    violation_date = Column(Date, nullable=False)
    severity = Column(Enum(ViolationSeverity), nullable=False)
    message = Column(String, nullable=False)
    resolved = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    shift_assignment = relationship("ShiftAssignment", back_populates="compliance_violations")
    rule = relationship("ComplianceRule", back_populates="violations")
    
    def __repr__(self):
        return f"<ComplianceViolation Assignment:{self.shift_assignment_id} Rule:{self.rule_id} ({self.severity.value})>"

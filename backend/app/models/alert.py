"""
Alert model - represents system alerts and notifications.
Phase 2 feature.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .base import Base


class AlertType(str, enum.Enum):
    """Type of alert"""
    CONFLICT = "conflict"
    COMPLIANCE = "compliance"
    UNASSIGNED = "unassigned"
    INSIGHT = "insight"
    OTHER = "other"


class AlertSeverity(str, enum.Enum):
    """Severity level of alert"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class InsightType(str, enum.Enum):
    """Type of insight (Phase 3)"""
    COMPLETION_RISK = "completion_risk"
    UNDERUTILIZATION = "underutilization"
    BURNOUT = "burnout"
    OPTIMIZATION = "optimization"


class Alert(Base):
    """Alert/notification model"""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    
    # Alert classification
    alert_type = Column(Enum(AlertType), nullable=False, index=True)
    severity = Column(Enum(AlertSeverity), nullable=False, index=True)
    
    # Content
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    
    # Phase 3: Insight-specific fields
    insight_type = Column(Enum(InsightType), nullable=True)
    recommended_action = Column(String, nullable=True)
    
    # Foreign keys (optional - alerts can be general or specific)
    related_shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=True, index=True)
    related_employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    
    # Status
    is_resolved = Column(Boolean, default=False, index=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    related_shift = relationship("Shift", back_populates="alerts")
    related_employee = relationship("Employee")
    
    def __repr__(self):
        return f"<Alert {self.alert_type.value} ({self.severity.value}): {self.title}>"

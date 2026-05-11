"""
Analytics models - for tracking activity and optimization feedback.
Phase 4 feature.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class ActivityLog(Base):
    """Activity log model - tracks actual business activity for learning"""
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Date/time information
    date = Column(Date, nullable=False, index=True)
    hour = Column(Integer, nullable=False)  # 0-23
    
    # Metrics
    actual_workload_metric = Column(Float, nullable=False)  # e.g., customers served, tasks completed
    scheduled_employees = Column(Integer, nullable=False)
    
    # Additional notes
    notes = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<ActivityLog {self.date} Hour:{self.hour} Workload:{self.actual_workload_metric}>"


class OptimizationFeedback(Base):
    """Optimization feedback model - tracks manager feedback for learning"""
    __tablename__ = "optimization_feedback"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    suggestion_id = Column(String, nullable=False, index=True)  # Reference to suggestion (could be UUID)
    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    
    # Feedback
    was_accepted = Column(Boolean, nullable=False)
    feedback_notes = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    manager = relationship("Employee")
    
    def __repr__(self):
        return f"<OptimizationFeedback Suggestion:{self.suggestion_id} Accepted:{self.was_accepted}>"

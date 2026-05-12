"""Alert repository - handles data access for Alert model"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime

from ..models.alert import Alert, AlertType, AlertSeverity
from .base import BaseRepository


class AlertRepository(BaseRepository[Alert]):
    """Repository for Alert model"""
    
    def __init__(self, db: Session):
        super().__init__(Alert, db)
    
    def get_unresolved(self, skip: int = 0, limit: int = 100) -> List[Alert]:
        """Get all unresolved alerts"""
        return self.db.query(Alert).filter(
            Alert.is_resolved == False
        ).order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_severity(self, severity: AlertSeverity, skip: int = 0, limit: int = 100) -> List[Alert]:
        """Get alerts by severity"""
        return self.db.query(Alert).filter(
            Alert.severity == severity
        ).order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_employee(self, employee_id: int, skip: int = 0, limit: int = 100) -> List[Alert]:
        """Get alerts related to a specific employee"""
        return self.db.query(Alert).filter(
            Alert.related_employee_id == employee_id
        ).order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_shift(self, shift_id: int) -> List[Alert]:
        """Get alerts related to a specific shift"""
        return self.db.query(Alert).filter(
            Alert.related_shift_id == shift_id
        ).all()
    
    def resolve_alert(self, alert_id: int) -> Optional[Alert]:
        """Mark an alert as resolved"""
        alert = self.get_by_id(alert_id)
        if alert:
            alert.is_resolved = True
            alert.resolved_at = func.now()
            self.db.commit()
            self.db.refresh(alert)
        return alert

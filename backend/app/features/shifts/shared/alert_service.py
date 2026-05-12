"""Alert Service - logic for managing system alerts and notifications"""

from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ....models.alert import Alert, AlertType, AlertSeverity
from ....repositories.alert_repository import AlertRepository


class AlertService:
    """Service to manage system alerts"""
    
    def __init__(self, db: Session):
        self.db = db
        self.alert_repo = AlertRepository(db)
    
    def create_alert(
        self,
        alert_type: AlertType,
        severity: AlertSeverity,
        title: str,
        message: str,
        related_shift_id: Optional[int] = None,
        related_employee_id: Optional[int] = None
    ) -> Alert:
        """Create a new alert"""
        alert = Alert(
            alert_type=alert_type,
            severity=severity,
            title=title,
            message=message,
            related_shift_id=related_shift_id,
            related_employee_id=related_employee_id
        )
        return self.alert_repo.create(alert)
    
    def get_active_alerts(self, skip: int = 0, limit: int = 100) -> List[Alert]:
        """Get all unresolved alerts"""
        return self.alert_repo.get_unresolved(skip, limit)
    
    def resolve_alert(self, alert_id: int) -> Optional[Alert]:
        """Resolve an alert"""
        return self.alert_repo.resolve_alert(alert_id)
    
    def get_alerts_by_type(self, alert_type: AlertType) -> List[Alert]:
        """Get alerts by type"""
        return self.db.query(Alert).filter(
            Alert.alert_type == alert_type,
            Alert.is_resolved == False
        ).all()

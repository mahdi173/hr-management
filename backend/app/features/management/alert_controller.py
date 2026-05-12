"""Alert Controller - endpoints for system alerts"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...database import get_db
from ..shifts.shared.alert_service import AlertService
from ...models.alert import AlertSeverity, AlertType

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("/", response_model=List[dict])
def get_alerts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all unresolved alerts"""
    service = AlertService(db)
    alerts = service.get_active_alerts(skip, limit)
    return [
        {
            "id": a.id,
            "alert_type": a.alert_type,
            "severity": a.severity,
            "title": a.title,
            "message": a.message,
            "related_shift_id": a.related_shift_id,
            "related_employee_id": a.related_employee_id,
            "created_at": a.created_at
        } for a in alerts
    ]


@router.put("/{alert_id}/resolve")
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """Mark an alert as resolved"""
    service = AlertService(db)
    alert = service.resolve_alert(alert_id)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with id {alert_id} not found"
        )
    return {"status": "success", "message": f"Alert {alert_id} resolved"}

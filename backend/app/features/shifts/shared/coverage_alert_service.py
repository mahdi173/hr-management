"""Coverage Alert Service - logic for identifying unassigned shifts and creating alerts"""

from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date

from ....repositories.shift_repository import ShiftRepository
from .alert_service import AlertService
from ....models.alert import AlertType, AlertSeverity


class CoverageAlertService:
    """Service to scan for shifts that are understaffed and create alerts"""
    
    def __init__(self, db: Session):
        self.db = db
        self.shift_repo = ShiftRepository(db)
        self.alert_service = AlertService(db)
    
    def scan_for_coverage_gaps(self, schedule_id: int) -> int:
        """
        Scan all shifts in a schedule for coverage gaps and create alerts.
        Returns the number of alerts created.
        """
        shifts = self.shift_repo.get_by_schedule(schedule_id, include_assignments=True, limit=1000)
        alerts_created = 0
        
        for shift in shifts:
            current_count = len(shift.assignments)
            
            if current_count < shift.min_employees:
                # Determine severity
                severity = AlertSeverity.WARNING
                if current_count == 0:
                    severity = AlertSeverity.ERROR
                
                title = "Shift Understaffed" if current_count > 0 else "Shift Unassigned"
                message = (
                    f"Shift on {shift.date} ({shift.start_time}-{shift.end_time}) "
                    f"has only {current_count}/{shift.min_employees} required employees."
                )
                
                # Check if an unresolved alert already exists for this shift and type
                existing_alerts = self.alert_service.get_alerts_by_type(AlertType.UNASSIGNED)
                already_alerted = any(a.related_shift_id == shift.id for a in existing_alerts)
                
                if not already_alerted:
                    self.alert_service.create_alert(
                        alert_type=AlertType.UNASSIGNED,
                        severity=severity,
                        title=title,
                        message=message,
                        related_shift_id=shift.id
                    )
                    alerts_created += 1
                    
        return alerts_created

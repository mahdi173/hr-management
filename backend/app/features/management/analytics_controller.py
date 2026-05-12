"""Analytics Controller - endpoints for workload and schedule health"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from ...database import get_db
from ..shifts.shared.analytics_service import AnalyticsService
from ..shifts.shared.coverage_alert_service import CoverageAlertService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/workload")
def get_workload_analysis(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db)
):
    """Analyze workload for all active employees"""
    service = AnalyticsService(db)
    return service.get_workload_analysis(start_date, end_date)


@router.get("/schedule/{schedule_id}/health")
def get_schedule_health(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    """Get health metrics for a specific schedule"""
    service = AnalyticsService(db)
    return service.get_schedule_health(schedule_id)


@router.post("/schedule/{schedule_id}/refresh-coverage-alerts")
def refresh_coverage_alerts(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    """Scan schedule for unassigned shifts and create alerts"""
    service = CoverageAlertService(db)
    count = service.scan_for_coverage_gaps(schedule_id)
    return {"status": "success", "alerts_created": count}

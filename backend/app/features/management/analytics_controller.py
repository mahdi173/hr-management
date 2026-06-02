"""Analytics Controller - endpoints for workload and schedule health"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from ...core.dependencies import require_manager
from ...database import get_db
from ...models.user import User
from ..shifts.shared.analytics_service import AnalyticsService
from ..shifts.shared.coverage_alert_service import CoverageAlertService
from ..shifts.shared.insight_service import InsightService
from ..shifts.shared.optimization_service import OptimizationService
from .learning_service import LearningService
from .preference_learning_service import PreferenceLearningService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/workload")
def get_workload_analysis(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_manager),
):
    """Analyze workload for all active employees"""
    service = AnalyticsService(db)
    return service.get_workload_analysis(start_date, end_date)


@router.get("/schedule/{schedule_id}/health")
def get_schedule_health(
    schedule_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_manager),
):
    """Get health metrics for a specific schedule"""
    service = AnalyticsService(db)
    return service.get_schedule_health(schedule_id)


@router.post("/schedule/{schedule_id}/refresh-coverage-alerts")
def refresh_coverage_alerts(
    schedule_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_manager),
):
    """Scan schedule for unassigned shifts and create alerts"""
    service = CoverageAlertService(db)
    count = service.scan_for_coverage_gaps(schedule_id)
    return {"status": "success", "alerts_created": count}


@router.post("/refresh-insights")
def refresh_insights(
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_manager),
):
    """Run proactive insight detection and create alerts"""
    service = InsightService(db)
    count = service.generate_all_insights()
    return {"status": "success", "insights_created": count}


@router.get("/rebalancing-suggestions")
def get_rebalancing_suggestions(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_manager),
):
    """Get suggestions to rebalance workload between employees"""
    service = OptimizationService(db)
    return service.get_rebalancing_suggestions(start_date, end_date)


# ========== Phase 4 - AI Learning Endpoints ========== #

@router.get("/learned-patterns")
def get_learned_patterns(
    lookback_months: int = Query(3, ge=1, le=12, description="Months of history to analyze"),
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_manager),
):
    """
    Analyze historical data to identify scheduling patterns.
    
    **Phase 4 Feature - US-4.2**
    
    Returns learned patterns including:
    - Optimal staffing by day of week and hour
    - Busy periods and slow periods  
    - Workload trends
    - Historical coverage quality
    
    Use this data to optimize future schedules based on past performance.
    """
    service = LearningService(db)
    return service.analyze_historical_patterns(lookback_months=lookback_months)


@router.get("/schedule/{schedule_id}/optimization-opportunities")
def get_optimization_opportunities(
    schedule_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_manager),
):
    """
    Compare schedule against learned patterns to identify improvements.
    
    **Phase 4 Feature - US-4.2**
    
    Identifies over/under-staffing based on historical optimal staffing levels.
    """
    service = LearningService(db)
    return {
        "schedule_id": schedule_id,
        "opportunities": service.identify_optimization_opportunities(schedule_id)
    }


@router.post("/learn-preferences")
def learn_employee_preferences(
    lookback_months: int = Query(3, ge=1, le=12),
    min_samples: int = Query(5, ge=3, le=20),
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_manager),
):
    """
    Analyze historical assignments to learn employee preferences.
    
    **Phase 4 Feature - US-4.3**
    
    Updates the assignment_preferences table with learned patterns:
    - Shift time preferences (morning/afternoon/evening/night)
    - Day of week preferences
    - Preferred colleague patterns
    
    Run this periodically (e.g., monthly) to keep preferences up-to-date.
    """
    service = PreferenceLearningService(db)
    results = service.learn_all_preferences(
        lookback_months=lookback_months,
        min_samples=min_samples
    )
    
    return {
        "status": "success",
        "employees_analyzed": len(results),
        "summary": {
            emp_id: {
                "employee_name": prefs["employee_name"],
                "assignments_analyzed": prefs["total_assignments_analyzed"],
                "shift_types_learned": len(prefs["shift_type_preferences"]),
                "preferred_colleagues": len(prefs["preferred_colleagues"])
            }
            for emp_id, prefs in results.items()
        }
    }


@router.get("/employees/{employee_id}/learned-preferences")
def get_employee_learned_preferences(
    employee_id: int,
    lookback_months: int = Query(3, ge=1, le=12),
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_manager),
):
    """
    Get learned scheduling preferences for a specific employee.
    
    **Phase 4 Feature - US-4.3**
    
    Returns detailed analysis of employee's historical assignment patterns.
    """
    service = PreferenceLearningService(db)
    return service.get_employee_preferences(employee_id, lookback_months=lookback_months)

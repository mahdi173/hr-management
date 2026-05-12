"""Get Schedule Views Controller - API endpoints for schedule visualization (US 1.9)"""

from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..shared.schedule_view_dto import DayView, WeekView, MonthView, ScheduleExport
from .get_schedule_views_usecase import GetScheduleViewsUseCase
from ....database import get_db


router = APIRouter()


@router.get(
    "/{schedule_id}/day-view",
    response_model=DayView,
    summary="Get day view of schedule",
    tags=["schedules", "views"]
)
def get_day_view(
    schedule_id: int,
    date: date = Query(..., description="Date to view (YYYY-MM-DD)"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    role_id: Optional[int] = Query(None, description="Filter by required role ID"),
    db: Session = Depends(get_db)
) -> DayView:
    """
    Get day view: all shifts for a specific date with assigned employees.
    
    - **schedule_id**: ID of the schedule
    - **date**: Date to view
    - **employee_id**: Optional filter to show only shifts for a specific employee
    - **role_id**: Optional filter to show only shifts requiring a specific role
    
    Returns all shifts for the date with employee assignments.
    
    This endpoint implements **US 1.9: Schedule Visualization - Day View**
    """
    use_case = GetScheduleViewsUseCase(db)
    return use_case.get_day_view(schedule_id, date, employee_id, role_id)


@router.get(
    "/{schedule_id}/week-view",
    response_model=WeekView,
    summary="Get week view of schedule",
    tags=["schedules", "views"]
)
def get_week_view(
    schedule_id: int,
    start_date: date = Query(..., description="First day of the week (YYYY-MM-DD)"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    role_id: Optional[int] = Query(None, description="Filter by required role ID"),
    db: Session = Depends(get_db)
) -> WeekView:
    """
    Get week view: shifts across 7 days starting from the given date.
    
    - **schedule_id**: ID of the schedule
    - **start_date**: First day of the week to view
    - **employee_id**: Optional filter to show only shifts for a specific employee
    - **role_id**: Optional filter to show only shifts requiring a specific role
    
    Returns 7 days of shifts organized by date.
    
    This endpoint implements **US 1.9: Schedule Visualization - Week View**
    """
    use_case = GetScheduleViewsUseCase(db)
    return use_case.get_week_view(schedule_id, start_date, employee_id, role_id)


@router.get(
    "/{schedule_id}/month-view",
    response_model=MonthView,
    summary="Get month view of schedule",
    tags=["schedules", "views"]
)
def get_month_view(
    schedule_id: int,
    year: int = Query(..., description="Year (e.g., 2026)"),
    month: int = Query(..., ge=1, le=12, description="Month (1-12)"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    role_id: Optional[int] = Query(None, description="Filter by required role ID"),
    db: Session = Depends(get_db)
) -> MonthView:
    """
    Get month view: shifts across an entire month organized by weeks.
    
    - **schedule_id**: ID of the schedule
    - **year**: Year to view
    - **month**: Month to view (1-12)
    - **employee_id**: Optional filter to show only shifts for a specific employee
    - **role_id**: Optional filter to show only shifts requiring a specific role
    
    Returns the entire month's shifts organized by weeks.
    
    This endpoint implements **US 1.9: Schedule Visualization - Month View**
    """
    use_case = GetScheduleViewsUseCase(db)
    return use_case.get_month_view(schedule_id, year, month, employee_id, role_id)


@router.get(
    "/{schedule_id}/export",
    response_model=ScheduleExport,
    summary="Export schedule data",
    tags=["schedules", "views"]
)
def export_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
) -> ScheduleExport:
    """
    Export complete schedule data in structured JSON format.
    
    - **schedule_id**: ID of the schedule to export
    
    Returns all shifts with complete details including assigned employees.
    Useful for external integrations or backups.
    
    This endpoint implements **US 1.9: Schedule Visualization - Export**
    """
    use_case = GetScheduleViewsUseCase(db)
    return use_case.export_schedule(schedule_id)

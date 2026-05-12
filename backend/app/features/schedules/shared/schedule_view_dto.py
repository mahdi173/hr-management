"""Schedule View Data Transfer Objects - For visualization features (US 1.9)"""

from pydantic import BaseModel, Field
from datetime import date as date_type
from typing import List, Optional


# ==================== Shift Summary for Views ====================

class ShiftSummaryForView(BaseModel):
    """Simplified shift info for schedule views"""
    shift_id: int
    start_time: str = Field(..., description="Start time in HH:MM format")
    end_time: str = Field(..., description="End time in HH:MM format")
    required_role_id: Optional[int] = None
    min_employees: int
    max_employees: int
    assigned_count: int = Field(..., description="Number of employees currently assigned")
    assigned_employees: List[dict] = Field(default_factory=list, description="List of assigned employee details")
    notes: Optional[str] = None


# ==================== Day View ====================

class DayView(BaseModel):
    """Day view: all shifts for a specific date"""
    date: date_type = Field(..., description="The date for this view")
    shifts: List[ShiftSummaryForView] = Field(default_factory=list, description="All shifts for this date")
    total_shifts: int = Field(..., description="Total number of shifts")
    total_employees_scheduled: int = Field(..., description="Total unique employees scheduled")


# ==================== Week View ====================

class WeekView(BaseModel):
    """Week view: shifts across 7 days"""
    start_date: date_type = Field(..., description="First day of the week (Monday)")
    end_date: date_type = Field(..., description="Last day of the week (Sunday)")
    days: List[DayView] = Field(..., description="Daily views for each day of the week")
    total_shifts: int = Field(..., description="Total shifts in the week")
    total_employees_scheduled: int = Field(..., description="Total unique employees scheduled in the week")


# ==================== Month View ====================

class MonthView(BaseModel):
    """Month view: shifts across an entire month"""
    year: int = Field(..., description="Year")
    month: int = Field(..., ge=1, le=12, description="Month (1-12)")
    start_date: date_type = Field(..., description="First day of the month")
    end_date: date_type = Field(..., description="Last day of the month")
    weeks: List[WeekView] = Field(..., description="Week views for the month")
    total_shifts: int = Field(..., description="Total shifts in the month")
    total_employees_scheduled: int = Field(..., description="Total unique employees scheduled in the month")


# ==================== Schedule Export ====================

class ScheduleExport(BaseModel):
    """Full schedule export in structured format"""
    schedule_id: int
    schedule_name: str
    schedule_start_date: date_type
    schedule_end_date: date_type
    total_shifts: int
    shifts: List[dict] = Field(..., description="Complete shift data with all details")

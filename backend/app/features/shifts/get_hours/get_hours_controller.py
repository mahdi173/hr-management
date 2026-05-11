"""Get Hours Controller - API endpoints for working hours tracking (US 1.8)"""

from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..shared.shift_dto import HoursSummary, ShiftWithHours
from .get_hours_usecase import GetHoursUseCase
from ....database import get_db


router = APIRouter()


@router.get(
    "/employees/{employee_id}/hours",
    response_model=HoursSummary,
    summary="Get working hours summary for employee",
    tags=["shifts", "employees"]
)
def get_employee_hours(
    employee_id: int,
    start_date: date = Query(..., description="Start date of the period"),
    end_date: date = Query(..., description="End date of the period"),
    db: Session = Depends(get_db)
) -> HoursSummary:
    """
    Get working hours summary for an employee in a date range.
    
    - **employee_id**: ID of the employee
    - **start_date**: Start date of the period
    - **end_date**: End date of the period
    
    Returns:
    - Total hours worked
    - Regular hours
    - Overtime hours
    - Number of shift assignments
    
    This endpoint implements **US 1.8: Working Hours Tracking**
    """
    use_case = GetHoursUseCase(db)
    return use_case.execute(employee_id, start_date, end_date)


@router.get(
    "/employees/{employee_id}/overtime",
    response_model=List[ShiftWithHours],
    summary="Get overtime shifts for employee",
    tags=["shifts", "employees"]
)
def get_employee_overtime(
    employee_id: int,
    start_date: Optional[date] = Query(None, description="Start date filter"),
    end_date: Optional[date] = Query(None, description="End date filter"),
    db: Session = Depends(get_db)
) -> List[ShiftWithHours]:
    """
    Get detailed list of overtime shifts for an employee.
    
    - **employee_id**: ID of the employee
    - **start_date**: Optional start date filter
    - **end_date**: Optional end date filter
    
    Returns list of shifts marked as overtime with:
    - Shift date and times
    - Calculated duration in hours
    - Assignment type
    
    This endpoint implements **US 1.8: Working Hours Tracking**
    """
    use_case = GetHoursUseCase(db)
    return use_case.get_overtime_details(employee_id, start_date, end_date)

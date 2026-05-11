"""Get Shifts Controller - API endpoints for retrieving shifts"""

from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..shared.shift_dto import ShiftResponse
from .get_shifts_usecase import GetShiftsUseCase
from ....database import get_db


router = APIRouter()


@router.get(
    "/shifts",
    response_model=List[ShiftResponse],
    summary="Get all shifts with filters",
    tags=["shifts"]
)
def get_shifts(
    schedule_id: Optional[int] = Query(None, description="Filter by schedule ID"),
    start_date: Optional[date] = Query(None, description="Filter by start date"),
    end_date: Optional[date] = Query(None, description="Filter by end date"),
    employee_id: Optional[int] = Query(None, description="Filter by assigned employee"),
    include_assignments: bool = Query(False, description="Include shift assignments"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    db: Session = Depends(get_db)
) -> List[ShiftResponse]:
    """
    Get shifts with optional filters:
    
    - **schedule_id**: Get shifts for a specific schedule
    - **start_date** and **end_date**: Get shifts within date range
    - **employee_id**: Get shifts assigned to an employee
    - **include_assignments**: Load shift assignments with each shift
    - **skip** and **limit**: Pagination parameters
    """
    use_case = GetShiftsUseCase(db)
    return use_case.execute(
        schedule_id=schedule_id,
        start_date=start_date,
        end_date=end_date,
        employee_id=employee_id,
        skip=skip,
        limit=limit,
        include_assignments=include_assignments
    )


@router.get(
    "/shifts/{shift_id}",
    response_model=ShiftResponse,
    summary="Get a specific shift",
    tags=["shifts"]
)
def get_shift(
    shift_id: int,
    include_assignments: bool = Query(False, description="Include shift assignments"),
    db: Session = Depends(get_db)
) -> ShiftResponse:
    """
    Get a specific shift by ID.
    
    - **shift_id**: ID of the shift to retrieve
    - **include_assignments**: Load shift assignments
    """
    use_case = GetShiftsUseCase(db)
    shift = use_case.get_one(shift_id, include_assignments)
    
    if not shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shift with id {shift_id} not found"
        )
    
    return shift

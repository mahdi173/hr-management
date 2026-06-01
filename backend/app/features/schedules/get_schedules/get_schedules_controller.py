"""Get Schedules Controller - HTTP endpoints for listing and retrieving schedules"""

from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from ....core.dependencies import get_current_user
from ....database import get_db
from ....models.user import User
from ..shared.schedule_dto import ScheduleResponse, ScheduleStatus
from .get_schedules_usecase import GetSchedulesUseCase

router = APIRouter()


@router.get("/", response_model=List[ScheduleResponse])
def list_schedules(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[ScheduleStatus] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user)
):
    """List schedules with optional filters"""
    use_case = GetSchedulesUseCase(db)
    return use_case.execute_list(start_date, end_date, status, skip, limit)


@router.get("/{schedule_id}", response_model=ScheduleResponse)
def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Get a single schedule by ID"""
    use_case = GetSchedulesUseCase(db)
    return use_case.execute_one(schedule_id)

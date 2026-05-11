"""Update Schedule Controller - HTTP endpoints for updating schedules"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared.schedule_dto import ScheduleUpdate, ScheduleResponse
from .update_schedule_usecase import UpdateScheduleUseCase

router = APIRouter()


@router.put("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(schedule_id: int, schedule_data: ScheduleUpdate, db: Session = Depends(get_db)):
    """
    Update an existing schedule
    
    Args:
        schedule_id: ID of the schedule to update
        schedule_data: Schedule update data
        db: Database session
        
    Returns:
        Updated schedule instance
    """
    use_case = UpdateScheduleUseCase(db)
    return use_case.execute(schedule_id, schedule_data)

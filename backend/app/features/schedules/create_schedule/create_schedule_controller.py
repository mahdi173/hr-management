"""Create Schedule Controller - HTTP endpoints for creating schedules"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ....core.dependencies import require_manager
from ....database import get_db
from ....models.user import User
from ..shared.schedule_dto import ScheduleCreate, ScheduleResponse
from .create_schedule_usecase import CreateScheduleUseCase

router = APIRouter()


@router.post("/", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_schedule(
    schedule_data: ScheduleCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_manager),
):
    """
    Create a new schedule
    
    Args:
        schedule_data: Schedule creation data
        db: Database session
        
    Returns:
        Created schedule instance
    """
    use_case = CreateScheduleUseCase(db)
    return use_case.execute(schedule_data)

"""Delete Schedule Controller - HTTP endpoints for deleting schedules"""

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from ....database import get_db
from .delete_schedule_usecase import DeleteScheduleUseCase

router = APIRouter()


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing schedule
    
    Args:
        schedule_id: ID of the schedule to delete
        db: Database session
        
    Returns:
        No content
    """
    use_case = DeleteScheduleUseCase(db)
    use_case.execute(schedule_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

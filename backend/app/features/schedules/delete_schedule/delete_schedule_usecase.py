"""Delete Schedule Use Case - Business logic for deleting schedules"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.schedule_repository import ScheduleRepository


class DeleteScheduleUseCase:
    """Use case for deleting an existing schedule"""

    def __init__(self, db: Session):
        self.repository = ScheduleRepository(db)

    def execute(self, schedule_id: int) -> bool:
        """
        Execute the delete schedule use case
        
        Args:
            schedule_id: ID of the schedule to delete
            
        Returns:
            True if deleted, False otherwise
        """
        # Validate schedule exists
        if not self.repository.exists(schedule_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Schedule with id {schedule_id} not found"
            )

        # Delete schedule
        return self.repository.delete(schedule_id)

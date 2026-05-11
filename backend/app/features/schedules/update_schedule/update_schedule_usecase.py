"""Update Schedule Use Case - Business logic for updating schedules"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.schedule_repository import ScheduleRepository
from ..shared.schedule_dto import ScheduleUpdate
from ....models.schedule import Schedule


class UpdateScheduleUseCase:
    """Use case for updating an existing schedule"""

    def __init__(self, db: Session):
        self.repository = ScheduleRepository(db)

    def execute(self, schedule_id: int, schedule_data: ScheduleUpdate) -> Schedule:
        """
        Execute the update schedule use case
        
        Args:
            schedule_id: ID of the schedule to update
            schedule_data: Schedule update data
            
        Returns:
            Updated schedule instance
        """
        # Validate schedule exists
        if not self.repository.exists(schedule_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Schedule with id {schedule_id} not found"
            )

        # Update schedule
        update_data = schedule_data.model_dump(exclude_unset=True)
        return self.repository.update(schedule_id, update_data)

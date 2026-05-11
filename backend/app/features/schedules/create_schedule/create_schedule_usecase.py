"""Create Schedule Use Case - Business logic for creating schedules"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.schedule_repository import ScheduleRepository
from ....repositories.employee_repository import EmployeeRepository
from ..shared.schedule_dto import ScheduleCreate
from ....models.schedule import Schedule


class CreateScheduleUseCase:
    """Use case for creating a new schedule"""

    def __init__(self, db: Session):
        self.repository = ScheduleRepository(db)
        self.employee_repo = EmployeeRepository(db)

    def execute(self, schedule_data: ScheduleCreate) -> Schedule:
        """
        Execute the create schedule use case
        
        Args:
            schedule_data: Schedule creation data
            
        Returns:
            Created schedule instance
        """
        # Validate creator exists
        if not self.employee_repo.exists(schedule_data.created_by_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with id {schedule_data.created_by_id} not found"
            )

        # Create schedule
        schedule_dict = schedule_data.model_dump()
        return self.repository.create(schedule_dict)

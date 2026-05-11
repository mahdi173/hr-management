"""Get Schedules Use Case - Business logic for listing and retrieving schedules"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date

from ....repositories.schedule_repository import ScheduleRepository
from ....models.schedule import Schedule, ScheduleStatus


class GetSchedulesUseCase:
    """Use case for listing or getting schedules"""

    def __init__(self, db: Session):
        self.repository = ScheduleRepository(db)

    def execute_list(self, 
                     start_date: Optional[date] = None, 
                     end_date: Optional[date] = None,
                     status: Optional[ScheduleStatus] = None,
                     skip: int = 0, 
                     limit: int = 100) -> List[Schedule]:
        """List schedules with optional filters"""
        if start_date and end_date:
            return self.repository.get_by_date_range(start_date, end_date)
        if status:
            return self.repository.get_by_status(status, skip, limit)
        return self.repository.get_all(skip, limit)

    def execute_one(self, schedule_id: int) -> Schedule:
        """Get a single schedule by ID"""
        schedule = self.repository.get_by_id(schedule_id)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Schedule with id {schedule_id} not found"
            )
        return schedule

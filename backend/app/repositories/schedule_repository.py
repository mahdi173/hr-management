"""
Schedule repository - handles data access for Schedule model.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import date

from ..models.schedule import Schedule, ScheduleStatus
from .base import BaseRepository


class ScheduleRepository(BaseRepository[Schedule]):
    """Repository for Schedule model with custom queries"""

    def __init__(self, db: Session):
        """Initialize with Schedule model"""
        super().__init__(Schedule, db)

    def get_by_date_range(self, start_date: date, end_date: date) -> List[Schedule]:
        """Get schedules that fall within or overlap a date range"""
        return self.db.query(self.model).filter(
            self.model.start_date <= end_date,
            self.model.end_date >= start_date
        ).all()

    def get_by_status(self, status: ScheduleStatus, skip: int = 0, limit: int = 100) -> List[Schedule]:
        """Get schedules by status"""
        return self.db.query(self.model).filter(
            self.model.status == status
        ).offset(skip).limit(limit).all()

    def get_by_created_by(self, employee_id: int) -> List[Schedule]:
        """Get schedules created by a specific employee"""
        return self.db.query(self.model).filter(
            self.model.created_by_id == employee_id
        ).all()

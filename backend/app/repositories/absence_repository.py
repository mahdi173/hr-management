"""
Absence repository - handles data access for Absence and AbsenceType models.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import date

from ..models.absence import Absence, AbsenceType, AbsenceStatus
from .base import BaseRepository


class AbsenceRepository(BaseRepository[Absence]):
    """Repository for Absence model with custom queries"""

    def __init__(self, db: Session):
        """Initialize with Absence model"""
        super().__init__(Absence, db)

    def get_by_employee(self, employee_id: int, skip: int = 0, limit: int = 100) -> List[Absence]:
        """Get absences for a specific employee"""
        return self.db.query(self.model).filter(
            self.model.employee_id == employee_id
        ).offset(skip).limit(limit).all()

    def get_by_status(self, status: AbsenceStatus, skip: int = 0, limit: int = 100) -> List[Absence]:
        """Get absences by status"""
        return self.db.query(self.model).filter(
            self.model.status == status
        ).offset(skip).limit(limit).all()

    def get_by_date_range(self, start_date: date, end_date: date) -> List[Absence]:
        """Get absences that overlap with a date range (all employees)"""
        return self.db.query(self.model).filter(
            and_(
                self.model.start_date <= end_date,
                self.model.end_date >= start_date,
                self.model.status == AbsenceStatus.APPROVED
            )
        ).all()

    def get_by_employee_and_date_range(
        self, 
        employee_id: int, 
        start_date: date, 
        end_date: date
    ) -> List[Absence]:
        """Get approved absences for a specific employee within a date range"""
        return self.db.query(self.model).filter(
            and_(
                self.model.employee_id == employee_id,
                self.model.start_date <= end_date,
                self.model.end_date >= start_date,
                self.model.status == AbsenceStatus.APPROVED
            )
        ).all()

    def get_pending_approvals(self, skip: int = 0, limit: int = 100) -> List[Absence]:
        """Get all pending absence requests"""
        return self.get_by_status(AbsenceStatus.PENDING, skip, limit)


class AbsenceTypeRepository(BaseRepository[AbsenceType]):
    """Repository for AbsenceType model"""

    def __init__(self, db: Session):
        """Initialize with AbsenceType model"""
        super().__init__(AbsenceType, db)

    def get_by_name(self, name: str) -> Optional[AbsenceType]:
        """Get absence type by name"""
        return self.db.query(self.model).filter(self.model.name == name).first()

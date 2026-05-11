"""Get Absences Use Case - Business logic for listing absence requests"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.absence_repository import AbsenceRepository
from ....models.absence import Absence, AbsenceStatus


class GetAbsencesUseCase:
    """Use case for listing or getting absence requests"""

    def __init__(self, db: Session):
        self.repository = AbsenceRepository(db)

    def execute_list(self, 
                     employee_id: Optional[int] = None, 
                     status: Optional[AbsenceStatus] = None,
                     skip: int = 0, 
                     limit: int = 100) -> List[Absence]:
        """List absences with optional filters"""
        if employee_id:
            return self.repository.get_by_employee(employee_id, skip, limit)
        if status:
            return self.repository.get_by_status(status, skip, limit)
        return self.repository.get_all(skip, limit)

    def execute_one(self, absence_id: int) -> Absence:
        """Get a single absence request by ID"""
        absence = self.repository.get_by_id(absence_id)
        if not absence:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Absence request with id {absence_id} not found"
            )
        return absence

"""Create Absence Use Case - Business logic for requesting absences"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date

from ....repositories.absence_repository import AbsenceRepository
from ....repositories.employee_repository import EmployeeRepository
from ..shared.absence_dto import AbsenceCreate
from ....models.absence import Absence, AbsenceType


class CreateAbsenceUseCase:
    """Use case for creating a new absence request"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = AbsenceRepository(db)
        self.employee_repo = EmployeeRepository(db)

    def execute(self, absence_data: AbsenceCreate) -> Absence:
        """
        Execute the create absence use case
        
        Args:
            absence_data: Absence creation data
            
        Returns:
            Created absence instance
            
        Raises:
            HTTPException: If employee or absence type doesn't exist
        """
        # Validate employee exists
        if not self.employee_repo.exists(absence_data.employee_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with id {absence_data.employee_id} not found"
            )

        # Validate absence type exists
        absence_type = self.db.query(AbsenceType).filter(
            AbsenceType.id == absence_data.absence_type_id
        ).first()
        if not absence_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Absence type with id {absence_data.absence_type_id} not found"
            )

        # Create absence
        absence_dict = absence_data.model_dump()
        
        # If the absence type doesn't require approval, set status to APPROVED immediately
        # However, for now we follow the AC: "Manager can approve or reject"
        # So we keep it PENDING by default (model default)
        
        return self.repository.create(absence_dict)

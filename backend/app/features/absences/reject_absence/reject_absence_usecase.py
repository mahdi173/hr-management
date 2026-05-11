"""Reject Absence Use Case - Business logic for rejecting absence requests"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.absence_repository import AbsenceRepository
from ....models.absence import Absence, AbsenceStatus


class RejectAbsenceUseCase:
    """Use case for rejecting a pending absence request"""

    def __init__(self, db: Session):
        self.repository = AbsenceRepository(db)

    def execute(self, absence_id: int) -> Absence:
        """
        Execute the reject absence use case
        
        Args:
            absence_id: ID of the absence request
            
        Returns:
            Updated absence instance
            
        Raises:
            HTTPException: If absence is not found or not pending
        """
        # Validate absence exists
        absence = self.repository.get_by_id(absence_id)
        if not absence:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Absence request with id {absence_id} not found"
            )

        # Validate status is PENDING
        if absence.status != AbsenceStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Absence request is already {absence.status.value}"
            )

        # Update status
        update_data = {
            "status": AbsenceStatus.REJECTED
        }
        return self.repository.update(absence_id, update_data)

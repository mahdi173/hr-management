"""Approve Absence Use Case - Business logic for approving absence requests"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.absence_repository import AbsenceRepository
from ....repositories.employee_repository import EmployeeRepository
from ....models.absence import Absence, AbsenceStatus


class ApproveAbsenceUseCase:
    """Use case for approving a pending absence request"""

    def __init__(self, db: Session):
        self.repository = AbsenceRepository(db)
        self.employee_repo = EmployeeRepository(db)

    def execute(self, absence_id: int, approved_by_id: int) -> Absence:
        """
        Execute the approve absence use case
        
        Args:
            absence_id: ID of the absence request
            approved_by_id: ID of the manager approving the request
            
        Returns:
            Updated absence instance
            
        Raises:
            HTTPException: If absence is not found, not pending, or manager not found
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

        # Validate manager exists
        if not self.employee_repo.exists(approved_by_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Manager with id {approved_by_id} not found"
            )

        # Update status
        update_data = {
            "status": AbsenceStatus.APPROVED,
            "approved_by_id": approved_by_id
        }
        return self.repository.update(absence_id, update_data)

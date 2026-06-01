"""Delete Shift Use Case - Business logic for deleting shifts"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.shift_repository import ShiftRepository


class DeleteShiftUseCase:
    """Use case for deleting an existing shift"""

    def __init__(self, db: Session):
        self.repository = ShiftRepository(db)

    def execute(self, shift_id: int) -> bool:
        """
        Execute the delete shift use case
        
        Args:
            shift_id: ID of the shift to delete
            
        Returns:
            True if deleted, False otherwise
        """
        # Validate shift exists
        if not self.repository.exists(shift_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shift with id {shift_id} not found"
            )

        # Delete shift
        return self.repository.delete(shift_id)

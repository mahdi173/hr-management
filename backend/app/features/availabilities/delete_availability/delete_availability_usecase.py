"""Delete Availability Use Case - Business logic for deleting availabilities"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.availability_repository import AvailabilityRepository


class DeleteAvailabilityUseCase:
    """Use case for deleting an availability"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = AvailabilityRepository(db)

    def execute(self, availability_id: int, hard_delete: bool = False) -> dict:
        """
        Execute the delete availability use case
        
        Args:
            availability_id: ID of the availability to delete
            hard_delete: If True, permanently delete; if False, soft delete (set is_active=False)
            
        Returns:
            Success message dictionary
            
        Raises:
            HTTPException: If availability is not found
        """
        # Check if availability exists
        availability = self.repository.get_by_id(availability_id)
        if not availability:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Availability with id {availability_id} not found"
            )

        if hard_delete:
            # Permanently delete the availability
            self.repository.delete(availability_id)
            return {"message": f"Availability {availability_id} permanently deleted"}
        else:
            # Soft delete - set is_active to False
            self.repository.update(availability_id, {"is_active": False})
            return {"message": f"Availability {availability_id} deactivated"}

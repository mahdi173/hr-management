"""Get One Availability Use Case - Business logic for retrieving a single availability"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.availability_repository import AvailabilityRepository
from ....models.availability import Availability


class GetOneAvailabilityUseCase:
    """Use case for retrieving a single availability by ID"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = AvailabilityRepository(db)

    def execute(self, availability_id: int) -> Availability:
        """
        Execute the get one availability use case
        
        Args:
            availability_id: ID of the availability to retrieve
            
        Returns:
            Availability instance
            
        Raises:
            HTTPException: If availability is not found
        """
        availability = self.repository.get_by_id(availability_id)
        
        if not availability:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Availability with id {availability_id} not found"
            )
        
        return availability

"""Update Availability Use Case - Business logic for updating availabilities"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.availability_repository import AvailabilityRepository
from ..shared.availability_dto import AvailabilityUpdate
from ....models.availability import Availability


class UpdateAvailabilityUseCase:
    """Use case for updating an existing availability"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = AvailabilityRepository(db)

    def execute(self, availability_id: int, availability_data: AvailabilityUpdate) -> Availability:
        """
        Execute the update availability use case
        
        Args:
            availability_id: ID of the availability to update
            availability_data: Updated availability data
            
        Returns:
            Updated availability instance
            
        Raises:
            HTTPException: If availability is not found or validation fails
        """
        # Check if availability exists
        availability = self.repository.get_by_id(availability_id)
        if not availability:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Availability with id {availability_id} not found"
            )

        # Get the update data, excluding unset fields
        update_dict = availability_data.model_dump(exclude_unset=True)

        if update_dict:
            # If updating times, check for overlaps
            if 'start_time' in update_dict or 'end_time' in update_dict:
                new_start_time = update_dict.get('start_time', availability.start_time)
                new_end_time = update_dict.get('end_time', availability.end_time)

                # Check for overlapping availabilities
                has_overlap = self.repository.check_overlap(
                    employee_id=availability.employee_id,
                    start_time=new_start_time,
                    end_time=new_end_time,
                    day_of_week=availability.day_of_week,
                    specific_date=availability.specific_date,
                    exclude_id=availability_id
                )

                if has_overlap:
                    if availability.is_recurring:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Updated availability overlaps with existing availability for day {availability.day_of_week}"
                        )
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Updated availability overlaps with existing availability for date {availability.specific_date}"
                        )

        # Update availability
        return self.repository.update(availability_id, update_dict)

"""Create Availability Use Case - Business logic for creating availabilities"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.availability_repository import AvailabilityRepository
from ....repositories.employee_repository import EmployeeRepository
from ..shared.availability_dto import AvailabilityCreate
from ....models.availability import Availability


class CreateAvailabilityUseCase:
    """Use case for creating a new availability"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = AvailabilityRepository(db)
        self.employee_repository = EmployeeRepository(db)

    def execute(self, availability_data: AvailabilityCreate) -> Availability:
        """
        Execute the create availability use case
        
        Args:
            availability_data: Availability creation data
            
        Returns:
            Created availability instance
            
        Raises:
            HTTPException: If employee doesn't exist or availability overlaps
        """
        # Check if employee exists
        employee = self.employee_repository.get_by_id(availability_data.employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with id {availability_data.employee_id} not found"
            )

        # Check for overlapping availabilities
        has_overlap = self.repository.check_overlap(
            employee_id=availability_data.employee_id,
            start_time=availability_data.start_time,
            end_time=availability_data.end_time,
            day_of_week=availability_data.day_of_week,
            specific_date=availability_data.specific_date
        )

        if has_overlap:
            if availability_data.is_recurring:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Availability overlaps with existing availability for day {availability_data.day_of_week}"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Availability overlaps with existing availability for date {availability_data.specific_date}"
                )

        # Create availability
        availability_dict = availability_data.model_dump()
        return self.repository.create(availability_dict)

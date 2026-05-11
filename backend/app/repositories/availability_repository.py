"""
Availability repository - handles data access for Availability model.
"""
from typing import Optional, List
from datetime import date, time
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..models.availability import Availability
from .base import BaseRepository


class AvailabilityRepository(BaseRepository[Availability]):
    """Repository for Availability model with custom queries"""

    def __init__(self, db: Session):
        """Initialize with Availability model"""
        super().__init__(Availability, db)

    def get_by_employee(self, employee_id: int, active_only: bool = True) -> List[Availability]:
        """
        Get all availabilities for a specific employee
        
        Args:
            employee_id: Employee ID
            active_only: If True, return only active availabilities
            
        Returns:
            List of availability instances
        """
        query = self.db.query(self.model).filter(self.model.employee_id == employee_id)
        if active_only:
            query = query.filter(self.model.is_active == True)
        return query.all()

    def get_by_day(self, employee_id: int, day_of_week: int) -> List[Availability]:
        """
        Get recurring availabilities for a specific day of week
        
        Args:
            employee_id: Employee ID
            day_of_week: Day of week (0-6, Monday-Sunday)
            
        Returns:
            List of availability instances
        """
        return self.db.query(self.model).filter(
            and_(
                self.model.employee_id == employee_id,
                self.model.day_of_week == day_of_week,
                self.model.is_recurring == True,
                self.model.is_active == True
            )
        ).all()

    def get_by_specific_date(self, employee_id: int, specific_date: date) -> List[Availability]:
        """
        Get availabilities for a specific date
        
        Args:
            employee_id: Employee ID
            specific_date: Specific date
            
        Returns:
            List of availability instances
        """
        return self.db.query(self.model).filter(
            and_(
                self.model.employee_id == employee_id,
                self.model.specific_date == specific_date,
                self.model.is_recurring == False,
                self.model.is_active == True
            )
        ).all()

    def check_overlap(
        self, 
        employee_id: int, 
        start_time: time, 
        end_time: time,
        day_of_week: Optional[int] = None,
        specific_date: Optional[date] = None,
        exclude_id: Optional[int] = None
    ) -> bool:
        """
        Check if a new availability overlaps with existing ones
        
        Args:
            employee_id: Employee ID
            start_time: Start time of the availability
            end_time: End time of the availability
            day_of_week: Day of week for recurring availability (0-6)
            specific_date: Specific date for non-recurring availability
            exclude_id: Optional availability ID to exclude from check (for updates)
            
        Returns:
            True if overlap exists, False otherwise
        """
        query = self.db.query(self.model).filter(
            and_(
                self.model.employee_id == employee_id,
                self.model.is_active == True,
                # Check for time overlap: (start1 < end2) AND (end1 > start2)
                self.model.start_time < end_time,
                self.model.end_time > start_time
            )
        )
        
        # Filter by recurring or specific date
        if day_of_week is not None:
            query = query.filter(
                and_(
                    self.model.day_of_week == day_of_week,
                    self.model.is_recurring == True
                )
            )
        elif specific_date is not None:
            query = query.filter(
                and_(
                    self.model.specific_date == specific_date,
                    self.model.is_recurring == False
                )
            )
        
        # Exclude specific availability (for updates)
        if exclude_id:
            query = query.filter(self.model.id != exclude_id)
        
        return query.first() is not None

    def get_recurring_availabilities(self, employee_id: int) -> List[Availability]:
        """
        Get all recurring availabilities for an employee
        
        Args:
            employee_id: Employee ID
            
        Returns:
            List of recurring availability instances
        """
        return self.db.query(self.model).filter(
            and_(
                self.model.employee_id == employee_id,
                self.model.is_recurring == True,
                self.model.is_active == True
            )
        ).all()

    def get_specific_date_availabilities(self, employee_id: int) -> List[Availability]:
        """
        Get all specific date availabilities for an employee
        
        Args:
            employee_id: Employee ID
            
        Returns:
            List of specific date availability instances
        """
        return self.db.query(self.model).filter(
            and_(
                self.model.employee_id == employee_id,
                self.model.is_recurring == False,
                self.model.is_active == True
            )
        ).all()

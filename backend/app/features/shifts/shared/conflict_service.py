"""Conflict Detection Service - logic for identifying scheduling conflicts"""

from datetime import date, time
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ....repositories.shift_repository import ShiftAssignmentRepository
from ....repositories.availability_repository import AvailabilityRepository
from ....repositories.absence_repository import AbsenceRepository
from .alert_service import AlertService
from ....models.alert import AlertType, AlertSeverity


class ConflictDetail(BaseModel):
    """Detailed information about a conflict"""
    type: str  # overlap, availability, absence
    message: str
    conflicting_entity_id: Optional[int] = None
    employee_id: int


class ConflictDetectionService:
    """Service to detect scheduling conflicts"""
    
    def __init__(self, db: Session):
        self.db = db
        self.assignment_repo = ShiftAssignmentRepository(db)
        self.availability_repo = AvailabilityRepository(db)
        self.absence_repo = AbsenceRepository(db)
        self.alert_service = AlertService(db)
    
    def notify_conflicts(self, conflicts: List[ConflictDetail], shift_id: Optional[int] = None) -> None:
        """Create persistent alerts for a list of conflicts"""
        for conflict in conflicts:
            self.alert_service.create_alert(
                alert_type=AlertType.CONFLICT,
                severity=AlertSeverity.ERROR,
                title=f"Scheduling Conflict: {conflict.type.capitalize()}",
                message=conflict.message,
                related_shift_id=shift_id,
                related_employee_id=conflict.employee_id
            )
    
    def check_all_conflicts(
        self,
        employee_id: int,
        shift_date: date,
        start_time: time,
        end_time: time,
        exclude_shift_id: Optional[int] = None
    ) -> List[ConflictDetail]:
        """Check for all types of conflicts for an employee and shift"""
        conflicts = []
        
        # 1. Overlap Conflicts
        overlap = self.check_overlap_conflicts(
            employee_id, shift_date, start_time, end_time, exclude_shift_id
        )
        if overlap:
            conflicts.append(overlap)
            
        # 2. Availability Conflicts
        availability = self.check_availability_conflicts(
            employee_id, shift_date, start_time, end_time
        )
        if availability:
            conflicts.append(availability)
            
        # 3. Absence Conflicts
        absence = self.check_absence_conflicts(
            employee_id, shift_date, shift_date
        )
        if absence:
            conflicts.append(absence)
            
        return conflicts

    def check_overlap_conflicts(
        self,
        employee_id: int,
        shift_date: date,
        start_time: time,
        end_time: time,
        exclude_shift_id: Optional[int] = None
    ) -> Optional[ConflictDetail]:
        """Check if employee has overlapping shift assignment"""
        has_conflict = self.assignment_repo.check_employee_conflict(
            employee_id=employee_id,
            shift_date=shift_date,
            start_time=start_time,
            end_time=end_time,
            exclude_shift_id=exclude_shift_id
        )
        
        if has_conflict:
            return ConflictDetail(
                type="overlap",
                message="Employee has an overlapping shift assignment",
                employee_id=employee_id
            )
        return None

    def check_availability_conflicts(
        self,
        employee_id: int,
        shift_date: date,
        start_time: time,
        end_time: time
    ) -> Optional[ConflictDetail]:
        """Check if employee is available during shift time"""
        day_of_week = shift_date.weekday()
        
        # Check specific date availability first
        specific = self.availability_repo.get_by_specific_date(
            employee_id=employee_id,
            specific_date=shift_date
        )
        
        if specific:
            is_available = False
            for avail in specific:
                if avail.start_time <= start_time and avail.end_time >= end_time:
                    is_available = True
                    break
            
            if not is_available:
                return ConflictDetail(
                    type="availability",
                    message="Employee is not available on this specific date",
                    employee_id=employee_id
                )
            return None
            
        # Check recurring availability
        recurring = self.availability_repo.get_by_day(
            employee_id=employee_id,
            day_of_week=day_of_week
        )
        
        if not recurring:
             return ConflictDetail(
                type="availability",
                message="Employee has no availability defined for this day of week",
                employee_id=employee_id
            )
            
        is_available = False
        for avail in recurring:
            if avail.start_time <= start_time and avail.end_time >= end_time:
                is_available = True
                break
                
        if not is_available:
            return ConflictDetail(
                type="availability",
                message="Employee is not available during this shift time (recurring availability)",
                employee_id=employee_id
            )
            
        return None

    def check_absence_conflicts(
        self,
        employee_id: int,
        start_date: date,
        end_date: date
    ) -> Optional[ConflictDetail]:
        """Check if employee has approved absences during date range"""
        employee_absences = self.absence_repo.get_by_employee_and_date_range(
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date
        )
        
        if employee_absences:
            return ConflictDetail(
                type="absence",
                message=f"Employee has an approved absence: {employee_absences[0].reason or 'No reason provided'}",
                conflicting_entity_id=employee_absences[0].id,
                employee_id=employee_id
            )
        return None

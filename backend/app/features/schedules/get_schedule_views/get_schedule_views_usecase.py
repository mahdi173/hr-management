"""Get Schedule Views Use Case - Business logic for schedule visualization (US 1.9)"""

from typing import Optional, List
from datetime import date, timedelta
from calendar import monthrange
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..shared.schedule_view_dto import DayView, WeekView, MonthView, ShiftSummaryForView, ScheduleExport
from ....repositories.shift_repository import ShiftRepository
from ....repositories.schedule_repository import ScheduleRepository
from ....models.shift import Shift


class GetScheduleViewsUseCase:
    """Use case for generating schedule visualization views"""
    
    def __init__(self, db: Session):
        self.db = db
        self.shift_repo = ShiftRepository(db)
        self.schedule_repo = ScheduleRepository(db)
    
    def get_day_view(
        self,
        schedule_id: int,
        view_date: date,
        employee_id: Optional[int] = None,
        role_id: Optional[int] = None
    ) -> DayView:
        """
        Get day view for a specific date
        
        Shows all shifts for a specific date with assigned employees
        """
        # Validate schedule exists
        schedule = self.schedule_repo.get_by_id(schedule_id)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Schedule with id {schedule_id} not found"
            )
        
        # Get shifts for the date
        shifts = self.shift_repo.get_shifts_for_date(
            schedule_id=schedule_id,
            shift_date=view_date,
            employee_id=employee_id,
            role_id=role_id
        )
        
        # Build shift summaries
        shift_summaries = self._build_shift_summaries(shifts)
        
        # Count unique employees
        unique_employees = set()
        for shift in shifts:
            for assignment in shift.assignments:
                unique_employees.add(assignment.employee_id)
        
        return DayView(
            date=view_date,
            shifts=shift_summaries,
            total_shifts=len(shifts),
            total_employees_scheduled=len(unique_employees)
        )
    
    def get_week_view(
        self,
        schedule_id: int,
        start_date: date,
        employee_id: Optional[int] = None,
        role_id: Optional[int] = None
    ) -> WeekView:
        """
        Get week view starting from a specific date
        
        Shows shifts across 7 days (Monday to Sunday)
        """
        # Validate schedule exists
        schedule = self.schedule_repo.get_by_id(schedule_id)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Schedule with id {schedule_id} not found"
            )
        
        # Calculate week end date (7 days from start)
        end_date = start_date + timedelta(days=6)
        
        # Get all shifts for the week
        shifts = self.shift_repo.get_shifts_for_week(
            schedule_id=schedule_id,
            start_date=start_date,
            end_date=end_date,
            employee_id=employee_id,
            role_id=role_id
        )
        
        # Group shifts by date
        shifts_by_date = {}
        for shift in shifts:
            if shift.date not in shifts_by_date:
                shifts_by_date[shift.date] = []
            shifts_by_date[shift.date].append(shift)
        
        # Build day views for each day
        day_views = []
        unique_employees = set()
        total_shifts = 0
        
        for day_offset in range(7):
            current_date = start_date + timedelta(days=day_offset)
            day_shifts = shifts_by_date.get(current_date, [])
            
            shift_summaries = self._build_shift_summaries(day_shifts)
            
            # Count employees for this day
            for shift in day_shifts:
                for assignment in shift.assignments:
                    unique_employees.add(assignment.employee_id)
            
            day_views.append(DayView(
                date=current_date,
                shifts=shift_summaries,
                total_shifts=len(day_shifts),
                total_employees_scheduled=len([a for s in day_shifts for a in s.assignments])
            ))
            
            total_shifts += len(day_shifts)
        
        return WeekView(
            start_date=start_date,
            end_date=end_date,
            days=day_views,
            total_shifts=total_shifts,
            total_employees_scheduled=len(unique_employees)
        )
    
    def get_month_view(
        self,
        schedule_id: int,
        year: int,
        month: int,
        employee_id: Optional[int] = None,
        role_id: Optional[int] = None
    ) -> MonthView:
        """
        Get month view for a specific year and month
        
        Shows shifts across the entire month, organized by weeks
        """
        # Validate schedule exists
        schedule = self.schedule_repo.get_by_id(schedule_id)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Schedule with id {schedule_id} not found"
            )
        
        # Get first and last day of month
        first_day = date(year, month, 1)
        last_day = date(year, month, monthrange(year, month)[1])
        
        # Get all shifts for the month
        shifts = self.shift_repo.get_shifts_for_month(
            schedule_id=schedule_id,
            year=year,
            month=month,
            employee_id=employee_id,
            role_id=role_id
        )
        
        # Build week views
        week_views = []
        unique_employees = set()
        total_shifts = len(shifts)
        
        # Start from the first Monday on or before the first day of the month
        current_start = first_day
        while current_start.weekday() != 0:  # 0 = Monday
            current_start = current_start - timedelta(days=1)
        
        # Generate weeks until we've covered the entire month
        while current_start <= last_day:
            week_end = current_start + timedelta(days=6)
            
            # Get week view
            week_view = self.get_week_view(
                schedule_id=schedule_id,
                start_date=current_start,
                employee_id=employee_id,
                role_id=role_id
            )
            
            week_views.append(week_view)
            
            # Track unique employees
            for day in week_view.days:
                for shift_summary in day.shifts:
                    for emp in shift_summary.assigned_employees:
                        unique_employees.add(emp.get('employee_id'))
            
            # Move to next week
            current_start = current_start + timedelta(days=7)
        
        return MonthView(
            year=year,
            month=month,
            start_date=first_day,
            end_date=last_day,
            weeks=week_views,
            total_shifts=total_shifts,
            total_employees_scheduled=len(unique_employees)
        )
    
    def export_schedule(self, schedule_id: int) -> ScheduleExport:
        """
        Export complete schedule data in structured format
        
        Returns all shifts with full details for export
        """
        # Validate schedule exists
        schedule = self.schedule_repo.get_by_id(schedule_id)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Schedule with id {schedule_id} not found"
            )
        
        # Get all shifts for the schedule
        shifts = self.shift_repo.get_by_schedule(
            schedule_id=schedule_id,
            include_assignments=True,
            limit=10000  # High limit for export
        )
        
        # Build complete shift data
        shift_data = []
        for shift in shifts:
            assigned_employees = [
                {
                    "employee_id": assignment.employee_id,
                    "employee_name": f"{assignment.employee.first_name} {assignment.employee.last_name}" if assignment.employee else "Unknown",
                    "status": assignment.status.value,
                    "assignment_type": assignment.assignment_type.value,
                    "is_overtime": assignment.is_overtime
                }
                for assignment in shift.assignments
            ]
            
            shift_data.append({
                "shift_id": shift.id,
                "date": shift.date.isoformat(),
                "start_time": shift.start_time.strftime("%H:%M"),
                "end_time": shift.end_time.strftime("%H:%M"),
                "required_role_id": shift.required_role_id,
                "min_employees": shift.min_employees,
                "max_employees": shift.max_employees,
                "notes": shift.notes,
                "assigned_employees": assigned_employees,
                "assigned_count": len(assigned_employees)
            })
        
        return ScheduleExport(
            schedule_id=schedule.id,
            schedule_name=schedule.name,
            schedule_start_date=schedule.start_date,
            schedule_end_date=schedule.end_date,
            total_shifts=len(shifts),
            shifts=shift_data
        )
    
    def _build_shift_summaries(self, shifts: List[Shift]) -> List[ShiftSummaryForView]:
        """Helper method to build shift summaries from shift models"""
        summaries = []
        
        for shift in shifts:
            assigned_employees = [
                {
                    "employee_id": assignment.employee_id,
                    "employee_name": f"{assignment.employee.first_name} {assignment.employee.last_name}" if assignment.employee else "Unknown",
                    "status": assignment.status.value
                }
                for assignment in shift.assignments
            ]
            
            summaries.append(ShiftSummaryForView(
                shift_id=shift.id,
                start_time=shift.start_time.strftime("%H:%M"),
                end_time=shift.end_time.strftime("%H:%M"),
                required_role_id=shift.required_role_id,
                min_employees=shift.min_employees,
                max_employees=shift.max_employees,
                assigned_count=len(assigned_employees),
                assigned_employees=assigned_employees,
                notes=shift.notes
            ))
        
        return summaries

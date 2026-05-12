"""Insight Service - logic for proactive scheduling intelligence"""

from datetime import date, timedelta, datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from ....repositories.shift_repository import ShiftRepository, ShiftAssignmentRepository
from ....repositories.employee_repository import EmployeeRepository
from ....repositories.schedule_repository import ScheduleRepository
from .alert_service import AlertService
from ....models.alert import AlertType, AlertSeverity, InsightType


class InsightService:
    """Service to generate proactive insights and alerts for managers"""
    
    def __init__(self, db: Session):
        self.db = db
        self.shift_repo = ShiftRepository(db)
        self.assignment_repo = ShiftAssignmentRepository(db)
        self.employee_repo = EmployeeRepository(db)
        self.schedule_repo = ScheduleRepository(db)
        self.alert_service = AlertService(db)
    
    def generate_all_insights(self) -> int:
        """Run all insight detection algorithms and return count of new alerts created"""
        count = 0
        count += self.detect_completion_risks()
        count += self.detect_burnout_risks()
        count += self.detect_underutilization_patterns()
        return count

    def detect_completion_risks(self) -> int:
        """Alert if schedules starting within 3 days are less than 80% complete"""
        today = date.today()
        three_days_from_now = today + timedelta(days=3)
        
        # Get schedules starting soon
        upcoming_schedules = self.schedule_repo.get_by_date_range(today, three_days_from_now)
        alerts_created = 0
        
        for schedule in upcoming_schedules:
            # We can use the logic from AnalyticsService or repeat it here
            shifts = self.shift_repo.get_by_schedule(schedule.id, include_assignments=True)
            if not shifts:
                continue
                
            total_required = sum(s.min_employees for s in shifts)
            total_assigned = sum(len(s.assignments) for s in shifts)
            
            completion_rate = (total_assigned / total_required) * 100 if total_required > 0 else 100
            
            if completion_rate < 80:
                title = f"High Completion Risk: {schedule.name}"
                message = f"Schedule is only {completion_rate:.1f}% complete and starts on {schedule.start_date}."
                
                # Check for existing unresolved insight for this schedule
                existing = self.db.query(AlertType).filter(
                    # We need to filter Alert model here
                ) # Simplified for now: just use alert_service to create
                
                self.alert_service.create_alert(
                    alert_type=AlertType.INSIGHT,
                    severity=AlertSeverity.ERROR,
                    title=title,
                    message=message,
                    insight_type=InsightType.COMPLETION_RISK,
                    recommended_action="Assign more employees or use AI recommendations to fill gaps."
                )
                alerts_created += 1
                
        return alerts_created

    def detect_burnout_risks(self) -> int:
        """Alert if employees are scheduled for more than 6 consecutive days"""
        # We'll check the current week and next week
        today = date.today()
        end_date = today + timedelta(days=14)
        
        employees = self.employee_repo.get_active_employees()
        alerts_created = 0
        
        for emp in employees:
            assignments = self.assignment_repo.get_by_employee(emp.id, today, end_date)
            if not assignments:
                continue
                
            # Track consecutive days
            dates_worked = sorted(list(set(a.shift.date for a in assignments)))
            if not dates_worked:
                continue
                
            consecutive_count = 1
            for i in range(1, len(dates_worked)):
                if dates_worked[i] == dates_worked[i-1] + timedelta(days=1):
                    consecutive_count += 1
                else:
                    consecutive_count = 1
                    
                if consecutive_count >= 6:
                    self.alert_service.create_alert(
                        alert_type=AlertType.INSIGHT,
                        severity=AlertSeverity.WARNING,
                        title=f"Burnout Risk: {emp.first_name} {emp.last_name}",
                        message=f"Employee is scheduled for {consecutive_count} consecutive days starting around {dates_worked[i-consecutive_count+1]}.",
                        insight_type=InsightType.BURNOUT,
                        recommended_action="Consider reassigning some shifts to other team members.",
                        related_employee_id=emp.id
                    )
                    alerts_created += 1
                    break # Only one alert per employee per scan
                    
        return alerts_created

    def detect_underutilization_patterns(self) -> int:
        """Alert if employees are consistently below 50% of their contract hours"""
        # Check the past 2 weeks
        end_date = date.today()
        start_date = end_date - timedelta(days=14)
        
        employees = self.employee_repo.get_active_employees()
        alerts_created = 0
        
        for emp in employees:
            if not emp.contract_type or emp.contract_type.weekly_hours == 0:
                continue
                
            stats = self.assignment_repo.get_hours_by_employee_and_period(emp.id, start_date, end_date)
            # Pro-rated contract hours for 2 weeks
            target_hours = emp.contract_type.weekly_hours * 2
            
            utilization = (stats["total_hours"] / target_hours) * 100 if target_hours > 0 else 100
            
            if utilization < 50:
                self.alert_service.create_alert(
                    alert_type=AlertType.INSIGHT,
                    severity=AlertSeverity.INFO,
                    title=f"Underutilization Pattern: {emp.first_name} {emp.last_name}",
                    message=f"Employee has worked only {utilization:.1f}% of contract hours over the last 2 weeks.",
                    insight_type=InsightType.UNDERUTILIZATION,
                    recommended_action="Review assignment distribution and availability.",
                    related_employee_id=emp.id
                )
                alerts_created += 1
                
        return alerts_created

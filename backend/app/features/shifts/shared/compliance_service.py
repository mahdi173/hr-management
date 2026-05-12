"""Compliance Service - logic for validating labor law and contract rules"""

from datetime import date, datetime, timedelta, time
from typing import List, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ....models.compliance import ComplianceRule, ComplianceViolation, RuleType, ViolationSeverity
from ....models.shift import ShiftAssignment
from ....repositories.shift_repository import ShiftAssignmentRepository
from ....repositories.employee_repository import EmployeeRepository
from .alert_service import AlertService
from ....models.alert import AlertType, AlertSeverity


class ComplianceResult(BaseModel):
    """Result of a compliance check"""
    is_valid: bool
    violations: List[str] = []
    errors: List[str] = []  # Blocking violations


class ComplianceService:
    """Service to validate scheduling compliance"""
    
    def __init__(self, db: Session):
        self.db = db
        self.assignment_repo = ShiftAssignmentRepository(db)
        self.employee_repo = EmployeeRepository(db)
        self.alert_service = AlertService(db)
    
    def notify_violations(self, result: ComplianceResult, employee_id: int, shift_id: Optional[int] = None) -> None:
        """Create persistent alerts for compliance violations"""
        # Create alerts for errors (blocking)
        for error in result.errors:
            self.alert_service.create_alert(
                alert_type=AlertType.COMPLIANCE,
                severity=AlertSeverity.ERROR,
                title="Labor Law Violation (Blocking)",
                message=error,
                related_shift_id=shift_id,
                related_employee_id=employee_id
            )
        
        # Create alerts for warnings (non-blocking)
        for warning in result.violations:
            self.alert_service.create_alert(
                alert_type=AlertType.COMPLIANCE,
                severity=AlertSeverity.WARNING,
                title="Labor Law Warning",
                message=warning,
                related_shift_id=shift_id,
                related_employee_id=employee_id
            )
    
    def validate_assignment(
        self,
        employee_id: int,
        shift_date: date,
        start_time: time,
        end_time: time,
        exclude_assignment_id: Optional[int] = None
    ) -> ComplianceResult:
        """Validate an assignment against all active compliance rules"""
        result = ComplianceResult(is_valid=True)
        
        # Get active rules
        rules = self.db.query(ComplianceRule).filter(ComplianceRule.is_active == True).all()
        
        # Calculate proposed duration
        start_dt = datetime.combine(shift_date, start_time)
        end_dt = datetime.combine(shift_date, end_time)
        duration_hours = (end_dt - start_dt).total_seconds() / 3600
        
        for rule in rules:
            if rule.rule_type == RuleType.MAX_DAILY_HOURS:
                # Check daily hours
                daily_stats = self.assignment_repo.get_hours_by_employee_and_period(
                    employee_id, shift_date, shift_date
                )
                total_daily = daily_stats["total_hours"] + duration_hours
                
                if total_daily > rule.threshold_value:
                    msg = f"Exceeds max daily hours ({total_daily:.1f}h > {rule.threshold_value}h)"
                    if rule.is_blocking:
                        result.errors.append(msg)
                        result.is_valid = False
                    else:
                        result.violations.append(msg)
                        
            elif rule.rule_type == RuleType.MAX_WEEKLY_HOURS:
                # Check weekly hours (assuming Monday start)
                start_of_week = shift_date - timedelta(days=shift_date.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                
                weekly_stats = self.assignment_repo.get_hours_by_employee_and_period(
                    employee_id, start_of_week, end_of_week
                )
                total_weekly = weekly_stats["total_hours"] + duration_hours
                
                if total_weekly > rule.threshold_value:
                    msg = f"Exceeds max weekly hours ({total_weekly:.1f}h > {rule.threshold_value}h)"
                    if rule.is_blocking:
                        result.errors.append(msg)
                        result.is_valid = False
                    else:
                        result.violations.append(msg)
                        
            elif rule.rule_type == RuleType.MIN_REST_HOURS:
                # Check rest period before and after
                # Before: find shift ending before start_time
                # After: find shift starting after end_time
                # This requires a bit more complex logic or repository helpers
                rest_conflict = self._check_rest_period_violation(
                    employee_id, shift_date, start_time, end_time, rule.threshold_value
                )
                if rest_conflict:
                    if rule.is_blocking:
                        result.errors.append(rest_conflict)
                        result.is_valid = False
                    else:
                        result.violations.append(rest_conflict)
        
        return result

    def _check_rest_period_violation(
        self,
        employee_id: int,
        shift_date: date,
        start_time: time,
        end_time: time,
        min_rest_hours: float
    ) -> Optional[str]:
        """Check for insufficient rest time between shifts"""
        # Check shift before
        # Find the latest shift for this employee that ends before the current shift starts
        # We check current day and previous day
        prev_day = shift_date - timedelta(days=1)
        assignments = self.assignment_repo.get_by_employee(employee_id, prev_day, shift_date)
        
        current_start_dt = datetime.combine(shift_date, start_time)
        current_end_dt = datetime.combine(shift_date, end_time)
        
        for assignment in assignments:
            s = assignment.shift
            s_start_dt = datetime.combine(s.date, s.start_time)
            s_end_dt = datetime.combine(s.date, s.end_time)
            
            # If shift ends before current starts
            if s_end_dt <= current_start_dt:
                rest_before = (current_start_dt - s_end_dt).total_seconds() / 3600
                if rest_before < min_rest_hours:
                    return f"Insufficient rest before shift ({rest_before:.1f}h < {min_rest_hours}h)"
            
            # If shift starts after current ends
            if s_start_dt >= current_end_dt:
                rest_after = (s_start_dt - current_end_dt).total_seconds() / 3600
                if rest_after < min_rest_hours:
                    return f"Insufficient rest after shift ({rest_after:.1f}h < {min_rest_hours}h)"
                    
        return None

    def log_violation(
        self,
        assignment_id: int,
        rule_id: int,
        violation_date: date,
        severity: ViolationSeverity,
        message: str
    ) -> ComplianceViolation:
        """Log a compliance violation to the database"""
        violation = ComplianceViolation(
            shift_assignment_id=assignment_id,
            rule_id=rule_id,
            violation_date=violation_date,
            severity=severity,
            message=message
        )
        self.db.add(violation)
        self.db.commit()
        self.db.refresh(violation)
        return violation

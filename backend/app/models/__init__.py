"""
Models package - contains all database models.
Organized by domain for team collaboration.
"""
from .base import Base

# Phase 1 - Personnel Management (Dev A)
from .employee import Employee
from .role import Role
from .contract_type import ContractType
from .availability import Availability
from .absence import AbsenceType, Absence, AbsenceStatus

# Phase 1 - Schedule Management (Dev B)
from .schedule import Schedule, ScheduleStatus
from .shift import Shift, ShiftAssignment, ShiftAssignmentStatus, AssignmentType

# Phase 2 - Compliance and Alerts
from .compliance import ComplianceRule, ComplianceViolation, RuleType, ViolationSeverity
from .alert import Alert, AlertType, AlertSeverity, InsightType

# Phase 3 - AI Recommendations
from .recommendation import AssignmentPreference

# Phase 4 - Advanced AI
from .schedule_template import ScheduleTemplate
from .analytics import ActivityLog, OptimizationFeedback
from .preference import EmployeePreference, PreferredColleague

# Infrastructure
from .user import User
from .item import Item  # Legacy - can be removed once new models are in use

__all__ = [
    # Base
    "Base",
    
    # Phase 1 - Personnel (Dev A)
    "Employee",
    "Role",
    "ContractType",
    "Availability",
    "AbsenceType",
    "Absence",
    "AbsenceStatus",
    
    # Phase 1 - Schedule (Dev B)
    "Schedule",
    "ScheduleStatus",
    "Shift",
    "ShiftAssignment",
    "ShiftAssignmentStatus",
    "AssignmentType",
    
    # Phase 2
    "ComplianceRule",
    "ComplianceViolation",
    "RuleType",
    "ViolationSeverity",
    "Alert",
    "AlertType",
    "AlertSeverity",
    "InsightType",
    
    # Phase 3
    "AssignmentPreference",
    
    # Phase 4
    "ScheduleTemplate",
    "ActivityLog",
    "OptimizationFeedback",
    "EmployeePreference",
    "PreferredColleague",
    
    # Infrastructure
    "User",
    "Item",  # Legacy
]

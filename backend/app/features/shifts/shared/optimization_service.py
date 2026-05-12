"""Optimization Service - logic for workload rebalancing and schedule optimization"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import date, timedelta
from pydantic import BaseModel

from ....repositories.shift_repository import ShiftAssignmentRepository, ShiftRepository
from ....repositories.employee_repository import EmployeeRepository
from .conflict_service import ConflictDetectionService
from .compliance_service import ComplianceService
from .analytics_service import AnalyticsService


class RebalancingSuggestion(BaseModel):
    """Suggestion to move a shift from one employee to another"""
    shift_id: int
    from_employee_id: int
    to_employee_id: int
    reason: str
    impact: str


class OptimizationService:
    """Service to identify and suggest schedule optimizations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.assignment_repo = ShiftAssignmentRepository(db)
        self.shift_repo = ShiftRepository(db)
        self.employee_repo = EmployeeRepository(db)
        self.conflict_service = ConflictDetectionService(db)
        self.compliance_service = ComplianceService(db)
        self.analytics_service = AnalyticsService(db)
    
    def get_rebalancing_suggestions(self, start_date: date, end_date: date) -> List[RebalancingSuggestion]:
        """Identify over-utilized employees and suggest moves to under-utilized ones"""
        workload = self.analytics_service.get_workload_analysis(start_date, end_date)
        
        # Identify target and source pools
        over_utilized = [w for w in workload if w.utilization_percentage > 110]
        under_utilized = [w for w in workload if w.utilization_percentage < 80]
        
        if not over_utilized or not under_utilized:
            return []
            
        suggestions = []
        
        for source in over_utilized:
            # Get shifts assigned to this employee
            assignments = self.assignment_repo.get_by_employee(source.employee_id, start_date, end_date)
            
            for target in under_utilized:
                # Try to find a shift that can be moved
                for assignment in assignments:
                    shift = assignment.shift
                    
                    # Check if target is available and has no conflicts
                    conflicts = self.conflict_service.check_all_conflicts(
                        employee_id=target.employee_id,
                        shift_date=shift.date,
                        start_time=shift.start_time,
                        end_time=shift.end_time
                    )
                    
                    if not conflicts:
                        # Check compliance for target
                        compliance = self.compliance_service.validate_assignment(
                            employee_id=target.employee_id,
                            shift_date=shift.date,
                            start_time=shift.start_time,
                            end_time=shift.end_time
                        )
                        
                        if not compliance.errors:
                            suggestions.append(RebalancingSuggestion(
                                shift_id=shift.id,
                                from_employee_id=source.employee_id,
                                to_employee_id=target.employee_id,
                                reason=f"{source.employee_name} is over-utilized ({source.utilization_percentage:.1f}%)",
                                impact=f"Moves {shift.date} shift to {target.employee_name} who has capacity ({target.utilization_percentage:.1f}%)"
                            ))
                            # Only suggest one move per source for now to keep it simple
                            break
                            
                if len(suggestions) >= 5: # Limit results
                    break
                    
        return suggestions

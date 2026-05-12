"""Analytics Service - logic for workload analysis and schedule health metrics"""

from datetime import date, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ....repositories.shift_repository import ShiftAssignmentRepository, ShiftRepository
from ....repositories.employee_repository import EmployeeRepository
from ....repositories.contract_type_repository import ContractTypeRepository


class WorkloadSummary(BaseModel):
    """Workload summary for an employee"""
    employee_id: int
    employee_name: str
    contract_hours: float
    scheduled_hours: float
    utilization_percentage: float
    status: str  # underutilized, balanced, overutilized


class ScheduleHealth(BaseModel):
    """Health metrics for a schedule"""
    schedule_id: int
    total_shifts: int
    fully_assigned_shifts: int
    completion_percentage: float
    unassigned_count: int


class AnalyticsService:
    """Service for workload and schedule analytics"""
    
    def __init__(self, db: Session):
        self.db = db
        self.assignment_repo = ShiftAssignmentRepository(db)
        self.shift_repo = ShiftRepository(db)
        self.employee_repo = EmployeeRepository(db)
    
    def get_workload_analysis(
        self,
        start_date: date,
        end_date: date
    ) -> List[WorkloadSummary]:
        """Analyze workload for all active employees in a period"""
        employees = self.employee_repo.get_active_employees()
        summaries = []
        
        for emp in employees:
            # Get hours
            stats = self.assignment_repo.get_hours_by_employee_and_period(
                emp.id, start_date, end_date
            )
            scheduled_hours = stats["total_hours"]
            
            # Get contract hours (pro-rated for the period if possible, 
            # but for now we assume weekly contract vs weekly period)
            contract_hours = 0.0
            if emp.contract_type:
                contract_hours = emp.contract_type.weekly_hours
            
            # Calculate utilization
            utilization = 0.0
            if contract_hours > 0:
                utilization = (scheduled_hours / contract_hours) * 100
            
            # Determine status
            status = "balanced"
            if utilization < 80:
                status = "underutilized"
            elif utilization > 110:
                status = "overutilized"
            
            summaries.append(WorkloadSummary(
                employee_id=emp.id,
                employee_name=f"{emp.first_name} {emp.last_name}",
                contract_hours=contract_hours,
                scheduled_hours=scheduled_hours,
                utilization_percentage=round(utilization, 1),
                status=status
            ))
            
        return summaries

    def get_schedule_health(self, schedule_id: int) -> ScheduleHealth:
        """Calculate health metrics for a specific schedule"""
        shifts = self.shift_repo.get_by_schedule(schedule_id, limit=1000)
        total_shifts = len(shifts)
        
        fully_assigned = 0
        unassigned_count = 0
        
        for shift in shifts:
            # Note: shift.assignments might need to be loaded
            # Repo get_by_schedule can include assignments
            current_count = len(shift.assignments)
            if current_count >= shift.min_employees:
                fully_assigned += 1
            if current_count == 0:
                unassigned_count += 1
                
        completion = 0.0
        if total_shifts > 0:
            completion = (fully_assigned / total_shifts) * 100
            
        return ScheduleHealth(
            schedule_id=schedule_id,
            total_shifts=total_shifts,
            fully_assigned_shifts=fully_assigned,
            completion_percentage=round(completion, 1),
            unassigned_count=unassigned_count
        )

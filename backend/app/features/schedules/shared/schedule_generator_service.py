"""
Schedule Generator Service - AI-powered schedule generation using OR-Tools
Phase 4 - US-4.1: Semi-Automatic Schedule Generation
"""
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from datetime import date, time, datetime, timedelta
from ortools.sat.python import cp_model
import logging

from ....models.employee import Employee
from ....models.role import Role
from ....models.shift import Shift
from ....models.schedule import Schedule
from ....repositories.employee_repository import EmployeeRepository
from ....repositories.shift_repository import ShiftRepository, ShiftAssignmentRepository
from ....repositories.schedule_repository import ScheduleRepository
from ...shifts.shared.conflict_service import ConflictDetectionService
from ...shifts.shared.compliance_service import ComplianceService

logger = logging.getLogger(__name__)


class ScheduleGenerationResult:
    """Result of schedule generation attempt"""
    def __init__(self):
        self.success: bool = False
        self.schedule_id: Optional[int] = None
        self.assignments: List[Dict] = []
        self.quality_score: float = 0.0
        self.warnings: List[str] = []
        self.errors: List[str] = []
        self.stats: Dict[str, Any] = {}
        self.solving_stats: Dict[str, Any] = {}


class ScheduleGeneratorService:
    """Generate optimized schedules using constraint programming"""
    
    def __init__(self, db: Session):
        self.db = db
        self.employee_repo = EmployeeRepository(db)
        self.shift_repo = ShiftRepository(db)
        self.assignment_repo = ShiftAssignmentRepository(db)
        self.schedule_repo = ScheduleRepository(db)
        self.conflict_service = ConflictDetectionService(db)
        self.compliance_service = ComplianceService(db)
    
    def generate_schedule(
        self,
        start_date: date,
        end_date: date,
        shift_requirements: List[Dict[str, Any]],
        schedule_name: Optional[str] = None,
        optimize_for_balance: bool = True
    ) -> ScheduleGenerationResult:
        """
        Generate an optimized schedule for the given date range.
        
        Args:
            start_date: Start date of schedule
            end_date: End date of schedule (inclusive)
            shift_requirements: List of shift templates with requirements
                Example: [
                    {
                        "date": "2026-06-10",
                        "start_time": "08:00",
                        "end_time": "12:00",
                        "required_role_id": 1,
                        "min_employees": 1,
                        "max_employees": 2
                    }
                ]
            schedule_name: Optional name for the schedule
            optimize_for_balance: Whether to optimize for workload balance
        
        Returns:
            ScheduleGenerationResult with assignments or errors
        """
        result = ScheduleGenerationResult()
        
        try:
            # Step 1: Create schedule object
            if not schedule_name:
                schedule_name = f"Generated {start_date.strftime('%Y-W%U')}"
            
            from ....models.schedule import ScheduleStatus
            schedule = Schedule(
                name=schedule_name,
                start_date=start_date,
                end_date=end_date,
                status=ScheduleStatus.DRAFT,
                created_by_id=1  # TODO: Get from auth context
            )
            self.db.add(schedule)
            self.db.flush()
            
            # Step 2: Create shifts from requirements
            shifts = self._create_shifts_from_requirements(schedule.id, shift_requirements)
            
            if not shifts:
                result.errors.append("No valid shifts created from requirements")
                return result
            
            # Step 3: Get available employees
            employees = self.employee_repo.get_active_employees()
            
            if not employees:
                result.errors.append("No active employees found")
                return result
            
            # Step 4: Build and solve constraint model
            logger.info(f"🤖 Generating schedule with {len(shifts)} shifts and {len(employees)} employees")
            assignments, stats = self._solve_assignment_problem(
                shifts, employees, optimize_for_balance
            )
            
            if not assignments:
                result.errors.append("Could not find feasible solution. Try relaxing constraints.")
                result.solving_stats = stats
                return result
            
            # Step 5: Create assignments in database
            created_assignments = []
            for shift_id, employee_id in assignments:
                from ....models.shift import ShiftAssignment
                assignment = ShiftAssignment(
                    shift_id=shift_id,
                    employee_id=employee_id
                )
                self.db.add(assignment)
                self.db.flush()
                created_assignments.append({
                    "shift_id": shift_id,
                    "employee_id": employee_id
                })
            
            # Step 6: Calculate quality metrics
            quality_score = self._calculate_quality_score(schedule.id, employees)
            
            # Step 7: Generate warnings
            warnings = self._generate_warnings(schedule.id, shifts)
            
            self.db.commit()
            
            # Build successful result
            result.success = True
            result.schedule_id = schedule.id
            result.assignments = created_assignments
            result.quality_score = quality_score
            result.warnings = warnings
            result.solving_stats = stats
            result.stats = {
                "total_shifts": len(shifts),
                "total_assignments": len(assignments),
                "employees_used": len(set(emp_id for _, emp_id in assignments)),
                "fill_rate": len(assignments) / sum(s.max_employees for s in shifts) * 100
            }
            
            logger.info(f"✅ Schedule generated successfully! Quality score: {quality_score:.2f}")
            
        except Exception as e:
            self.db.rollback()
            result.errors.append(f"Generation failed: {str(e)}")
            logger.error(f"❌ Schedule generation error: {e}", exc_info=True)
        
        return result
    
    def _create_shifts_from_requirements(
        self, 
        schedule_id: int, 
        requirements: List[Dict[str, Any]]
    ) -> List[Shift]:
        """Create Shift objects from requirement specifications"""
        shifts = []
        
        for req in requirements:
            try:
                shift_date = datetime.strptime(req["date"], "%Y-%m-%d").date() if isinstance(req["date"], str) else req["date"]
                start_time = datetime.strptime(req["start_time"], "%H:%M").time() if isinstance(req["start_time"], str) else req["start_time"]
                end_time = datetime.strptime(req["end_time"], "%H:%M").time() if isinstance(req["end_time"], str) else req["end_time"]
                
                shift = Shift(
                    schedule_id=schedule_id,
                    date=shift_date,
                    start_time=start_time,
                    end_time=end_time,
                    required_role_id=req.get("required_role_id", 1),
                    min_employees=req.get("min_employees", 1),
                    max_employees=req.get("max_employees", 1),
                    is_active=True
                )
                self.db.add(shift)
                shifts.append(shift)
                
            except Exception as e:
                logger.warning(f"Skipping invalid shift requirement: {e}")
                continue
        
        self.db.flush()  # Get shift IDs
        return shifts
    
    def _solve_assignment_problem(
        self,
        shifts: List[Shift],
        employees: List[Employee],
        optimize_for_balance: bool
    ) -> Tuple[List[Tuple[int, int]], Dict[str, Any]]:
        """
        Solve the shift assignment problem using OR-Tools CP-SAT.
        
        Returns:
            Tuple of (assignments, solving_stats)
            assignments: List of (shift_id, employee_id) tuples
        """
        model = cp_model.CpModel()
        
        # Decision variables: assignment[shift_id][employee_id] = 1 if assigned
        assignment_vars = {}
        for shift in shifts:
            for employee in employees:
                var_name = f"shift_{shift.id}_emp_{employee.id}"
                assignment_vars[(shift.id, employee.id)] = model.NewBoolVar(var_name)
        
        # Constraint 1: Each shift must have min-max employees
        for shift in shifts:
            shift_assignments = [assignment_vars[(shift.id, emp.id)] for emp in employees]
            model.Add(sum(shift_assignments) >= shift.min_employees)
            model.Add(sum(shift_assignments) <= shift.max_employees)
        
        # Constraint 2: No overlapping shifts for same employee
        for employee in employees:
            # Group shifts by date for efficiency
            shifts_by_date = {}
            for shift in shifts:
                if shift.date not in shifts_by_date:
                    shifts_by_date[shift.date] = []
                shifts_by_date[shift.date].append(shift)
            
            # Check overlaps within each day
            for day_shifts in shifts_by_date.values():
                for i, shift1 in enumerate(day_shifts):
                    for shift2 in day_shifts[i+1:]:
                        if self._shifts_overlap(shift1, shift2):
                            # Can't be assigned to both overlapping shifts
                            model.Add(
                                assignment_vars[(shift1.id, employee.id)] +
                                assignment_vars[(shift2.id, employee.id)] <= 1
                            )
        
        # Constraint 3: Respect employee availability and absences
        for shift in shifts:
            for employee in employees:
                if not self._is_employee_available(employee, shift):
                    # Force assignment to 0
                    model.Add(assignment_vars[(shift.id, employee.id)] == 0)
        
        # Constraint 4: Weekly hour limits (simplified - per employee per week)
        # Group shifts by week
        weeks = {}
        for shift in shifts:
            week_key = shift.date.strftime("%Y-W%U")
            if week_key not in weeks:
                weeks[week_key] = []
            weeks[week_key].append(shift)
        
        for employee in employees:
            max_weekly_hours = 40.0  # Default fallback
            if employee.contract_type:
                max_weekly_hours = employee.contract_type.max_weekly_hours or (employee.contract_type.weekly_hours * 1.2)
            
            for week_shifts in weeks.values():
                weekly_hours_expr = []
                for shift in week_shifts:
                    shift_hours = self._calculate_shift_hours(shift)
                    weekly_hours_expr.append(
                        assignment_vars[(shift.id, employee.id)] * int(shift_hours * 10)  # Scale to int
                    )
                if weekly_hours_expr:
                    model.Add(sum(weekly_hours_expr) <= int(max_weekly_hours * 10))
        
        # Objective: Optimize for workload balance if requested
        if optimize_for_balance:
            # Minimize variance in hours worked
            # We'll use a simpler approach: maximize minimum hours and minimize maximum hours
            employee_hours = []
            for employee in employees:
                hours_expr = []
                for shift in shifts:
                    shift_hours = self._calculate_shift_hours(shift)
                    hours_expr.append(
                        assignment_vars[(shift.id, employee.id)] * int(shift_hours * 10)
                    )
                if hours_expr:
                    employee_hours.append(sum(hours_expr))
            
            # Try to balance by minimizing the range
            # (This is simplified; production would use more sophisticated objectives)
            if employee_hours:
                min_hours = model.NewIntVar(0, 1000, "min_hours")
                max_hours = model.NewIntVar(0, 1000, "max_hours")
                
                for hours in employee_hours:
                    model.Add(hours >= min_hours)
                    model.Add(hours <= max_hours)
                
                # Minimize range while maximizing coverage
                model.Minimize(max_hours - min_hours)
        
        # Solve
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 30.0  # 30 second timeout
        
        status = solver.Solve(model)
        
        # Extract solution
        assignments = []
        stats = {
            "status": solver.StatusName(status),
            "solve_time": solver.WallTime(),
            "optimal": status == cp_model.OPTIMAL
        }
        
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            for shift in shifts:
                for employee in employees:
                    if solver.Value(assignment_vars[(shift.id, employee.id)]) == 1:
                        assignments.append((shift.id, employee.id))
            
            logger.info(f"✓ Found solution: {len(assignments)} assignments in {stats['solve_time']:.2f}s")
        else:
            logger.warning(f"⚠️  No solution found. Status: {stats['status']}")
        
        return assignments, stats
    
    def _shifts_overlap(self, shift1: Shift, shift2: Shift) -> bool:
        """Check if two shifts overlap in time"""
        if shift1.date != shift2.date:
            return False
        
        start1 = datetime.combine(shift1.date, shift1.start_time)
        end1 = datetime.combine(shift1.date, shift1.end_time)
        start2 = datetime.combine(shift2.date, shift2.start_time)
        end2 = datetime.combine(shift2.date, shift2.end_time)
        
        return start1 < end2 and start2 < end1
    
    def _is_employee_available(self, employee: Employee, shift: Shift) -> bool:
        """Check if employee is available for this shift (simplified)"""
        # Check absences
        conflicts = self.conflict_service.check_all_conflicts(
            employee_id=employee.id,
            shift_date=shift.date,
            start_time=shift.start_time,
            end_time=shift.end_time
        )
        
        if conflicts:
            return False
        
        # Check compliance (basic)
        compliance = self.compliance_service.validate_assignment(
            employee_id=employee.id,
            shift_date=shift.date,
            start_time=shift.start_time,
            end_time=shift.end_time
        )
        
        return not compliance.errors
    
    def _calculate_shift_hours(self, shift: Shift) -> float:
        """Calculate duration of shift in hours"""
        start = datetime.combine(date.today(), shift.start_time)
        end = datetime.combine(date.today(), shift.end_time)
        return (end - start).seconds / 3600
    
    def _calculate_quality_score(self, schedule_id: int, employees: List[Employee]) -> float:
        """Calculate overall quality score for generated schedule (0-1)"""
        score = 0.0
        weights = []
        
        # Metric 1: Coverage rate (how many shifts are filled)
        shifts = self.shift_repo.get_by_schedule(schedule_id)
        required_assignments = sum(s.min_employees for s in shifts)
        actual_assignments = sum(len(self.assignment_repo.get_by_shift(s.id)) for s in shifts)
        
        coverage_score = min(1.0, actual_assignments / required_assignments) if required_assignments > 0 else 0.0
        score += coverage_score * 0.4
        weights.append(0.4)
        
        # Metric 2: Workload balance (variance in hours)
        employee_hours = []
        for emp in employees:
            total_hours = 0.0
            for shift in shifts:
                assignments = self.assignment_repo.get_by_shift(shift.id)
                if any(a.employee_id == emp.id for a in assignments):
                    total_hours += self._calculate_shift_hours(shift)
            if total_hours > 0:
                employee_hours.append(total_hours)
        
        if employee_hours:
            avg_hours = sum(employee_hours) / len(employee_hours)
            variance = sum((h - avg_hours) ** 2 for h in employee_hours) / len(employee_hours)
            balance_score = max(0, 1 - (variance / (avg_hours ** 2))) if avg_hours > 0 else 0.5
            score += balance_score * 0.3
            weights.append(0.3)
        
        # Metric 3: No conflicts
        conflict_count = 0
        for shift in shifts:
            assignments = self.assignment_repo.get_by_shift(shift.id)
            for assignment in assignments:
                conflicts = self.conflict_service.check_all_conflicts(
                    employee_id=assignment.employee_id,
                    shift_date=shift.date,
                    start_time=shift.start_time,
                    end_time=shift.end_time
                )
                conflict_count += len(conflicts)
        
        conflict_score = max(0, 1 - (conflict_count / max(1, len(shifts))))
        score += conflict_score * 0.3
        weights.append(0.3)
        
        # Normalize by total weight
        total_weight = sum(weights)
        return score / total_weight if total_weight > 0 else 0.0
    
    def _generate_warnings(self, schedule_id: int, shifts: List[Shift]) -> List[str]:
        """Generate warnings about potential issues"""
        warnings = []
        
        for shift in shifts:
            assignments = self.assignment_repo.get_by_shift(shift.id)
            
            # Warn if shift is under-staffed
            if len(assignments) < shift.min_employees:
                warnings.append(
                    f"Shift on {shift.date} at {shift.start_time} is under-staffed "
                    f"({len(assignments)}/{shift.min_employees})"
                )
            
            # Warn if compliance issues
            for assignment in assignments:
                compliance = self.compliance_service.validate_assignment(
                    employee_id=assignment.employee_id,
                    shift_date=shift.date,
                    start_time=shift.start_time,
                    end_time=shift.end_time
                )
                if compliance.warnings:
                    warnings.extend([f"Shift {shift.id}: {w}" for w in compliance.warnings[:2]])
        
        return warnings[:10]  # Limit to top 10 warnings

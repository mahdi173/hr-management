"""Unit tests for ShiftRepository and ShiftAssignmentRepository"""

import pytest
from datetime import date, time, datetime
from app.repositories.shift_repository import ShiftRepository, ShiftAssignmentRepository
from app.repositories.schedule_repository import ScheduleRepository
from app.repositories.employee_repository import EmployeeRepository
from app.models.shift import ShiftAssignmentStatus, AssignmentType


class TestShiftRepository:
    """Tests for ShiftRepository"""
    
    def test_create_shift(self, db_session):
        """Test creating a shift"""
        # Create schedule first
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create({
            "name": "Week 1",
            "start_date": date(2026, 5, 11),
            "end_date": date(2026, 5, 17),
            "created_by_id": 1
        })
        
        # Create shift
        shift_repo = ShiftRepository(db_session)
        shift = shift_repo.create({
            "schedule_id": schedule.id,
            "date": date(2026, 5, 12),
            "start_time": time(9, 0),
            "end_time": time(17, 0),
            "min_employees": 1,
            "max_employees": 3,
            "notes": "Morning shift"
        })
        
        assert shift.id is not None
        assert shift.schedule_id == schedule.id
        assert shift.date == date(2026, 5, 12)
        assert shift.min_employees == 1
    
    def test_get_by_schedule(self, db_session):
        """Test getting shifts for a schedule"""
        # Create schedule
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create({
            "name": "Week 1",
            "start_date": date(2026, 5, 11),
            "end_date": date(2026, 5, 17),
            "created_by_id": 1
        })
        
        # Create multiple shifts
        shift_repo = ShiftRepository(db_session)
        for i in range(3):
            shift_repo.create({
                "schedule_id": schedule.id,
                "date": date(2026, 5, 12 + i),
                "start_time": time(9, 0),
                "end_time": time(17, 0)
            })
        
        # Get shifts
        shifts = shift_repo.get_by_schedule(schedule.id)
        assert len(shifts) == 3
    
    def test_get_by_date_range(self, db_session):
        """Test getting shifts within a date range"""
        # Create schedule
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create({
            "name": "Week 1",
            "start_date": date(2026, 5, 11),
            "end_date": date(2026, 5, 20),
            "created_by_id": 1
        })
        
        # Create shifts across different dates
        shift_repo = ShiftRepository(db_session)
        shift_repo.create({
            "schedule_id": schedule.id,
            "date": date(2026, 5, 11),
            "start_time": time(9, 0),
            "end_time": time(17, 0)
        })
        shift_repo.create({
            "schedule_id": schedule.id,
            "date": date(2026, 5, 15),
            "start_time": time(9, 0),
            "end_time": time(17, 0)
        })
        shift_repo.create({
            "schedule_id": schedule.id,
            "date": date(2026, 5, 20),
            "start_time": time(9, 0),
            "end_time": time(17, 0)
        })
        
        # Get shifts in range
        shifts = shift_repo.get_by_date_range(
            start_date=date(2026, 5, 12),
            end_date=date(2026, 5, 18)
        )
        assert len(shifts) == 1
        assert shifts[0].date == date(2026, 5, 15)
    
    def test_get_by_date(self, db_session):
        """Test getting all shifts for a specific date"""
        # Create schedule
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create({
            "name": "Week 1",
            "start_date": date(2026, 5, 11),
            "end_date": date(2026, 5, 17),
            "created_by_id": 1
        })
        
        # Create multiple shifts on same date
        shift_repo = ShiftRepository(db_session)
        shift_repo.create({
            "schedule_id": schedule.id,
            "date": date(2026, 5, 12),
            "start_time": time(9, 0),
            "end_time": time(13, 0)
        })
        shift_repo.create({
            "schedule_id": schedule.id,
            "date": date(2026, 5, 12),
            "start_time": time(14, 0),
            "end_time": time(18, 0)
        })
        
        # Get shifts
        shifts = shift_repo.get_by_date(date(2026, 5, 12))
        assert len(shifts) == 2


class TestShiftAssignmentRepository:
    """Tests for ShiftAssignmentRepository"""
    
    def test_create_assignment(self, db_session):
        """Test creating a shift assignment"""
        # Setup: create schedule and shift
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create({
            "name": "Week 1",
            "start_date": date(2026, 5, 11),
            "end_date": date(2026, 5, 17),
            "created_by_id": 1
        })
        
        shift_repo = ShiftRepository(db_session)
        shift = shift_repo.create({
            "schedule_id": schedule.id,
            "date": date(2026, 5, 12),
            "start_time": time(9, 0),
            "end_time": time(17, 0)
        })
        
        # Create assignment
        assignment_repo = ShiftAssignmentRepository(db_session)
        created = assignment_repo.create({
            "shift_id": shift.id,
            "employee_id": 1,
            "assignment_type": AssignmentType.REGULAR
        })
        
        assert created.id is not None
        assert created.shift_id == shift.id
        assert created.employee_id == 1
        assert created.status == ShiftAssignmentStatus.ASSIGNED
    
    def test_get_by_shift(self, db_session):
        """Test getting assignments for a shift"""
        # Setup
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create({
            "name": "Week 1",
            "start_date": date(2026, 5, 11),
            "end_date": date(2026, 5, 17),
            "created_by_id": 1
        })
        
        shift_repo = ShiftRepository(db_session)
        shift = shift_repo.create({
            "schedule_id": schedule.id,
            "date": date(2026, 5, 12),
            "start_time": time(9, 0),
            "end_time": time(17, 0),
            "max_employees": 3
        })
        
        # Create multiple assignments
        assignment_repo = ShiftAssignmentRepository(db_session)
        for emp_id in [1, 2]:
            assignment_repo.create({
                "shift_id": shift.id,
                "employee_id": emp_id
            })
        
        # Get assignments
        assignments = assignment_repo.get_by_shift(shift.id)
        assert len(assignments) == 2
    
    def test_check_employee_conflict(self, db_session):
        """Test checking for overlapping shift assignments"""
        # Setup
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create({
            "name": "Week 1",
            "start_date": date(2026, 5, 11),
            "end_date": date(2026, 5, 17),
            "created_by_id": 1
        })
        
        shift_repo = ShiftRepository(db_session)
        shift1 = shift_repo.create({
            "schedule_id": schedule.id,
            "date": date(2026, 5, 12),
            "start_time": time(9, 0),
            "end_time": time(17, 0)
        })
        
        # Assign employee to shift
        assignment_repo = ShiftAssignmentRepository(db_session)
        assignment_repo.create({
            "shift_id": shift1.id,
            "employee_id": 1
        })
        
        # Check for conflict with overlapping time
        has_conflict = assignment_repo.check_employee_conflict(
            employee_id=1,
            shift_date=date(2026, 5, 12),
            start_time=time(10, 0),  # Overlaps with 9:00-17:00
            end_time=time(14, 0)
        )
        assert has_conflict is True
        
        # Check for non-overlapping time
        no_conflict = assignment_repo.check_employee_conflict(
            employee_id=1,
            shift_date=date(2026, 5, 12),
            start_time=time(18, 0),  # After 17:00
            end_time=time(22, 0)
        )
        assert no_conflict is False
    
    def test_get_hours_by_employee_and_period(self, db_session):
        """Test calculating hours for an employee"""
        # Setup
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create({
            "name": "Week 1",
            "start_date": date(2026, 5, 11),
            "end_date": date(2026, 5, 17),
            "created_by_id": 1
        })
        
        shift_repo = ShiftRepository(db_session)
        assignment_repo = ShiftAssignmentRepository(db_session)
        
        # Create shift 1: 8 hours regular
        shift1 = shift_repo.create({
            "schedule_id": schedule.id,
            "date": date(2026, 5, 12),
            "start_time": time(9, 0),
            "end_time": time(17, 0)
        })
        assignment_repo.create({
            "shift_id": shift1.id,
            "employee_id": 1,
            "is_overtime": False
        })
        
        # Create shift 2: 4 hours overtime
        shift2 = shift_repo.create({
            "schedule_id": schedule.id,
            "date": date(2026, 5, 13),
            "start_time": time(18, 0),
            "end_time": time(22, 0)
        })
        assignment_repo.create({
            "shift_id": shift2.id,
            "employee_id": 1,
            "is_overtime": True
        })
        
        # Calculate hours
        hours = assignment_repo.get_hours_by_employee_and_period(
            employee_id=1,
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17)
        )
        
        assert hours['total_hours'] == 12.0
        assert hours['regular_hours'] == 8.0
        assert hours['overtime_hours'] == 4.0
        assert hours['assignment_count'] == 2
    
    def test_count_assignments_for_shift(self, db_session):
        """Test counting assignments for a shift"""
        # Setup
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create({
            "name": "Week 1",
            "start_date": date(2026, 5, 11),
            "end_date": date(2026, 5, 17),
            "created_by_id": 1
        })
        
        shift_repo = ShiftRepository(db_session)
        shift = shift_repo.create({
            "schedule_id": schedule.id,
            "date": date(2026, 5, 12),
            "start_time": time(9, 0),
            "end_time": time(17, 0),
            "max_employees": 5
        })
        
        # Create assignments
        assignment_repo = ShiftAssignmentRepository(db_session)
        for emp_id in [1, 2, 3]:
            assignment_repo.create({
                "shift_id": shift.id,
                "employee_id": emp_id
            })
        
        # Count
        count = assignment_repo.count_assignments_for_shift(shift.id)
        assert count == 3

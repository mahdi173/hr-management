"""Tests for Schedule Views Feature - US 1.9"""

import pytest
from datetime import date, time, timedelta
from fastapi.testclient import TestClient
from app.models.schedule import Schedule
from app.models.employee import Employee
from app.models.shift import Shift, ShiftAssignment
from app.repositories.schedule_repository import ScheduleRepository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.shift_repository import ShiftRepository, ShiftAssignmentRepository


class TestScheduleViews:
    """Test schedule visualization views"""
    
    def test_get_day_view_success(self, client: TestClient, db_session):
        """Test getting day view for a specific date"""
        # Create test data using repository
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1 Schedule",
            description="Test schedule",
            start_date=date(2026, 1, 5),
            end_date=date(2026, 1, 11),
            created_by_id=1,
            status="published"
        ))
        schedule_id = schedule.id
        
        # Create employee using repository
        employee_repo = EmployeeRepository(db_session)
        employee = employee_repo.create(Employee(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            role_id=1,
            contract_type_id=1,
            is_active=True
        ))
        employee_id = employee.id
        
        # Create shift using repository
        shift_repo = ShiftRepository(db_session)
        shift = shift_repo.create(Shift(
            schedule_id=schedule_id,
            date=date(2026, 1, 5),
            start_time=time(9, 0),
            end_time=time(17, 0),
            required_role_id=1,
            min_employees=1,
            max_employees=3,
            notes="Morning shift"
        ))
        shift_id = shift.id
        
        # Assign employee using repository
        assignment_repo = ShiftAssignmentRepository(db_session)
        assignment_repo.create(ShiftAssignment(
            shift_id=shift_id,
            employee_id=employee_id
        ))
        
        # Get day view
        response = client.get(f"/api/v1/schedules/{schedule_id}/day-view?date=2026-01-05")
        
        assert response.status_code == 200
        data = response.json()
        assert data["date"] == "2026-01-05"
        assert data["total_shifts"] == 1
        assert data["total_employees_scheduled"] == 1
        assert len(data["shifts"]) == 1
        assert data["shifts"][0]["shift_id"] == shift_id
        assert data["shifts"][0]["assigned_count"] == 1
        assert len(data["shifts"][0]["assigned_employees"]) == 1
    
    def test_get_day_view_no_shifts(self, client: TestClient, db_session):
        """Test day view with no shifts on that date"""
        # Create schedule using repository
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Empty Schedule",
            description="Test",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 31),
            created_by_id=1,
            status="published"
        ))
        schedule_id = schedule.id
        
        # Get day view for date with no shifts
        response = client.get(f"/api/v1/schedules/{schedule_id}/day-view?date=2026-01-15")
        
        assert response.status_code == 200
        data = response.json()
        assert data["date"] == "2026-01-15"
        assert data["total_shifts"] == 0
        assert data["total_employees_scheduled"] == 0
        assert len(data["shifts"]) == 0
    
    def test_get_day_view_invalid_schedule(self, client: TestClient):
        """Test day view with non-existent schedule"""
        response = client.get("/api/v1/schedules/99999/day-view?date=2026-01-01")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_get_day_view_with_employee_filter(self, client: TestClient, db_session):
        """Test day view filtered by employee"""
        # Create schedule using repository
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Test Schedule",
            description="Test",
            start_date=date(2026, 1, 5),
            end_date=date(2026, 1, 11),
            created_by_id=1,
            status="published"
        ))
        schedule_id = schedule.id
        
        # Create two employees using repository
        employee_repo = EmployeeRepository(db_session)
        emp1 = employee_repo.create(Employee(
            first_name="Alice",
            last_name="Smith",
            email="alice@example.com",
            phone="111",
            role_id=1,
            contract_type_id=1,
            is_active=True
        ))
        emp2 = employee_repo.create(Employee(
            first_name="Bob",
            last_name="Jones",
            email="bob@example.com",
            phone="222",
            role_id=1,
            contract_type_id=1,
            is_active=True
        ))
        emp1_id = emp1.id
        emp2_id = emp2.id
        
        # Create two shifts using repository
        shift_repo = ShiftRepository(db_session)
        shift1 = shift_repo.create(Shift(
            schedule_id=schedule_id,
            date=date(2026, 1, 5),
            start_time=time(9, 0),
            end_time=time(17, 0),
            required_role_id=1,
            min_employees=1,
            max_employees=2
        ))
        shift2 = shift_repo.create(Shift(
            schedule_id=schedule_id,
            date=date(2026, 1, 5),
            start_time=time(17, 0),
            end_time=time(23, 0),
            required_role_id=1,
            min_employees=1,
            max_employees=2
        ))
        shift1_id = shift1.id
        shift2_id = shift2.id
        
        # Assign employees using repository
        assignment_repo = ShiftAssignmentRepository(db_session)
        assignment_repo.create(ShiftAssignment(shift_id=shift1_id, employee_id=emp1_id))
        assignment_repo.create(ShiftAssignment(shift_id=shift2_id, employee_id=emp2_id))
        
        # Get day view filtered by emp1
        response = client.get(f"/api/v1/schedules/{schedule_id}/day-view?date=2026-01-05&employee_id={emp1_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_shifts"] == 1  # Only shift1 should be returned
        assert data["shifts"][0]["shift_id"] == shift1_id
    
    def test_get_week_view_success(self, client: TestClient, db_session):
        """Test getting week view"""
        # Create schedule using repository
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week Schedule",
            description="Test",
            start_date=date(2026, 1, 5),
            end_date=date(2026, 1, 18),
            created_by_id=1,
            status="published"
        ))
        schedule_id = schedule.id
        
        # Create employee using repository
        employee_repo = EmployeeRepository(db_session)
        emp = employee_repo.create(Employee(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            phone="123",
            role_id=1,
            contract_type_id=1,
            is_active=True
        ))
        emp_id = emp.id
        
        # Create shifts for multiple days using repository
        shift_repo = ShiftRepository(db_session)
        assignment_repo = ShiftAssignmentRepository(db_session)
        for day_offset in range(3):  # Create shifts for 3 days
            shift_date = date(2026, 1, 5) + timedelta(days=day_offset)
            shift = shift_repo.create(Shift(
                schedule_id=schedule_id,
                date=shift_date,
                start_time=time(9, 0),
                end_time=time(17, 0),
                required_role_id=1,
                min_employees=1,
                max_employees=2
            ))
            assignment_repo.create(ShiftAssignment(shift_id=shift.id, employee_id=emp_id))
        
        # Get week view
        response = client.get(f"/api/v1/schedules/{schedule_id}/week-view?start_date=2026-01-05")
        
        assert response.status_code == 200
        data = response.json()
        assert data["start_date"] == "2026-01-05"
        assert data["end_date"] == "2026-01-11"  # 7 days from start
        assert data["total_shifts"] == 3
        assert data["total_employees_scheduled"] == 1
        assert len(data["days"]) == 7  # Should have 7 days
        
        # Check that we have shifts on the first 3 days
        assert data["days"][0]["total_shifts"] == 1
        assert data["days"][1]["total_shifts"] == 1
        assert data["days"][2]["total_shifts"] == 1
        # And no shifts on the rest
        assert data["days"][3]["total_shifts"] == 0
    
    def test_get_month_view_success(self, client: TestClient, db_session):
        """Test getting month view"""
        # Create schedule using repository
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="January Schedule",
            description="Test",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 31),
            created_by_id=1,
            status="published"
        ))
        schedule_id = schedule.id
        
        # Create employee using repository
        employee_repo = EmployeeRepository(db_session)
        emp = employee_repo.create(Employee(
            first_name="Test",
            last_name="User",
            email="month@example.com",
            phone="999",
            role_id=1,
            contract_type_id=1,
            is_active=True
        ))
        emp_id = emp.id
        
        # Create a few shifts throughout the month using repository
        shift_repo = ShiftRepository(db_session)
        assignment_repo = ShiftAssignmentRepository(db_session)
        shift_dates = [date(2026, 1, 5), date(2026, 1, 15), date(2026, 1, 25)]
        for shift_date in shift_dates:
            shift = shift_repo.create(Shift(
                schedule_id=schedule_id,
                date=shift_date,
                start_time=time(9, 0),
                end_time=time(17, 0),
                required_role_id=1,
                min_employees=1,
                max_employees=2
            ))
            assignment_repo.create(ShiftAssignment(shift_id=shift.id, employee_id=emp_id))
        
        # Get month view
        response = client.get(f"/api/v1/schedules/{schedule_id}/month-view?year=2026&month=1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["year"] == 2026
        assert data["month"] == 1
        assert data["start_date"] == "2026-01-01"
        assert data["end_date"] == "2026-01-31"
        assert data["total_shifts"] == 3
        assert data["total_employees_scheduled"] >= 1
        assert len(data["weeks"]) >= 4  # January 2026 spans multiple weeks
    
    def test_export_schedule_success(self, client: TestClient, db_session):
        """Test exporting schedule data"""
        # Create schedule using repository
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Export Test Schedule",
            description="For export testing",
            start_date=date(2026, 2, 1),
            end_date=date(2026, 2, 7),
            created_by_id=1,
            status="published"
        ))
        schedule_id = schedule.id
        
        # Create employee using repository
        employee_repo = EmployeeRepository(db_session)
        emp = employee_repo.create(Employee(
            first_name="Export",
            last_name="Test",
            email="export@example.com",
            phone="777",
            role_id=1,
            contract_type_id=1,
            is_active=True
        ))
        emp_id = emp.id
        
        # Create shift using repository
        shift_repo = ShiftRepository(db_session)
        shift = shift_repo.create(Shift(
            schedule_id=schedule_id,
            date=date(2026, 2, 1),
            start_time=time(9, 0),
            end_time=time(17, 0),
            required_role_id=1,
            min_employees=1,
            max_employees=2,
            notes="Test shift for export"
        ))
        shift_id = shift.id
        assignment_repo = ShiftAssignmentRepository(db_session)
        assignment_repo.create(ShiftAssignment(shift_id=shift_id, employee_id=emp_id))
        
        # Export schedule
        response = client.get(f"/api/v1/schedules/{schedule_id}/export")
        
        assert response.status_code == 200
        data = response.json()
        assert data["schedule_id"] == schedule_id
        assert data["schedule_name"] == "Export Test Schedule"
        assert data["schedule_start_date"] == "2026-02-01"
        assert data["schedule_end_date"] == "2026-02-07"
        assert data["total_shifts"] == 1
        assert len(data["shifts"]) == 1
        
        # Verify shift details in export
        shift_export = data["shifts"][0]
        assert shift_export["shift_id"] == shift_id
        assert shift_export["date"] == "2026-02-01"
        assert shift_export["start_time"] == "09:00"
        assert shift_export["end_time"] == "17:00"
        assert shift_export["notes"] == "Test shift for export"
        assert shift_export["assigned_count"] == 1
        assert len(shift_export["assigned_employees"]) == 1
        assert shift_export["assigned_employees"][0]["employee_id"] == emp_id
    
    def test_export_schedule_not_found(self, client: TestClient):
        """Test exporting non-existent schedule"""
        response = client.get("/api/v1/schedules/99999/export")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_get_week_view_invalid_schedule(self, client: TestClient):
        """Test week view with non-existent schedule"""
        response = client.get("/api/v1/schedules/99999/week-view?start_date=2026-01-05")
        
        assert response.status_code == 404
    
    def test_get_month_view_invalid_schedule(self, client: TestClient):
        """Test month view with non-existent schedule"""
        response = client.get("/api/v1/schedules/99999/month-view?year=2026&month=1")
        
        assert response.status_code == 404

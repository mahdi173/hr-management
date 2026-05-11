"""Unit tests for working hours tracking endpoints (US 1.8)"""

import pytest
from datetime import date, time
from app.models.schedule import Schedule
from app.models.availability import Availability
from app.repositories.schedule_repository import ScheduleRepository
from app.repositories.availability_repository import AvailabilityRepository


class TestGetEmployeeHours:
    """Tests for GET /employees/{id}/hours endpoint"""
    
    def test_get_hours_summary_success(self, db_session, client):
        """Test getting hours summary for an employee"""
        # Create schedule
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
        # Create availability
        avail_repo = AvailabilityRepository(db_session)
        avail_repo.create(Availability(
            employee_id=1,
            day_of_week=0,  # Monday
            start_time=time(8, 0),
            end_time=time(20, 0),
            is_recurring=True,
            is_active=True
        ))
        avail_repo.create(Availability(
            employee_id=1,
            day_of_week=1,  # Tuesday
            start_time=time(8, 0),
            end_time=time(20, 0),
            is_recurring=True,
            is_active=True
        ))
        
        # Create shift 1: Monday 9-17 (8 hours regular)
        shift1_response = client.post(
            f"/api/v1/schedules/{schedule.id}/shifts",
            json={
                "schedule_id": schedule.id,
                "date": "2026-05-12",  # Monday
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "min_employees": 1,
                "max_employees": 3
            }
        )
        shift1_id = shift1_response.json()["id"]
        
        # Create shift 2: Tuesday 9-13 (4 hours regular)
        shift2_response = client.post(
            f"/api/v1/schedules/{schedule.id}/shifts",
            json={
                "schedule_id": schedule.id,
                "date": "2026-05-13",  # Tuesday
                "start_time": "09:00:00",
                "end_time": "13:00:00",
                "min_employees": 1,
                "max_employees": 3
            }
        )
        shift2_id = shift2_response.json()["id"]
        
        # Create shift 3: Tuesday evening (4 hours overtime)
        shift3_response = client.post(
            f"/api/v1/schedules/{schedule.id}/shifts",
            json={
                "schedule_id": schedule.id,
                "date": "2026-05-13",  # Tuesday
                "start_time": "18:00:00",
                "end_time": "22:00:00",
                "min_employees": 1,
                "max_employees": 3
            }
        )
        shift3_id = shift3_response.json()["id"]
        
        # Assign employee to all shifts
        client.post(
            f"/api/v1/shifts/{shift1_id}/assign",
            json={
                "shift_id": shift1_id,
                "employee_id": 1,
                "assignment_type": "regular",
                "is_overtime": False
            }
        )
        client.post(
            f"/api/v1/shifts/{shift2_id}/assign",
            json={
                "shift_id": shift2_id,
                "employee_id": 1,
                "assignment_type": "regular",
                "is_overtime": False
            }
        )
        client.post(
            f"/api/v1/shifts/{shift3_id}/assign",
            json={
                "shift_id": shift3_id,
                "employee_id": 1,
                "assignment_type": "overtime",
                "is_overtime": True
            }
        )
        
        # Get hours summary
        response = client.get(
            "/api/v1/employees/1/hours?start_date=2026-05-11&end_date=2026-05-17"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["employee_id"] == 1
        assert data["period_start"] == "2026-05-11"
        assert data["period_end"] == "2026-05-17"
        assert data["total_hours"] == 16.0  # 8 + 4 + 4
        assert data["regular_hours"] == 12.0  # 8 + 4
        assert data["overtime_hours"] == 4.0  # 4
        assert data["assignment_count"] == 3
    
    def test_get_hours_employee_not_found(self, db_session, client):
        """Test getting hours for non-existent employee"""
        response = client.get(
            "/api/v1/employees/99999/hours?start_date=2026-05-11&end_date=2026-05-17"
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_get_hours_invalid_date_range(self, db_session, client):
        """Test getting hours with invalid date range"""
        response = client.get(
            "/api/v1/employees/1/hours?start_date=2026-05-20&end_date=2026-05-10"
        )
        
        assert response.status_code == 400
        assert "before" in response.json()["detail"].lower()
    
    def test_get_hours_no_assignments(self, db_session, client):
        """Test getting hours when employee has no assignments"""
        response = client.get(
            "/api/v1/employees/1/hours?start_date=2026-05-11&end_date=2026-05-17"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_hours"] == 0.0
        assert data["regular_hours"] == 0.0
        assert data["overtime_hours"] == 0.0
        assert data["assignment_count"] == 0


class TestGetEmployeeOvertime:
    """Tests for GET /employees/{id}/overtime endpoint"""
    
    def test_get_overtime_success(self, db_session, client):
        """Test getting overtime shifts for an employee"""
        # Create schedule
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
        # Create availability
        avail_repo = AvailabilityRepository(db_session)
        avail_repo.create(Availability(
            employee_id=1,
            day_of_week=0,
            start_time=time(8, 0),
            end_time=time(23, 0),
            is_recurring=True,
            is_active=True
        ))
        
        # Create regular shift
        regular_shift_response = client.post(
            f"/api/v1/schedules/{schedule.id}/shifts",
            json={
                "schedule_id": schedule.id,
                "date": "2026-05-12",
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "min_employees": 1,
                "max_employees": 3
            }
        )
        regular_shift_id = regular_shift_response.json()["id"]
        
        # Create overtime shift
        overtime_shift_response = client.post(
            f"/api/v1/schedules/{schedule.id}/shifts",
            json={
                "schedule_id": schedule.id,
                "date": "2026-05-12",
                "start_time": "18:00:00",
                "end_time": "22:00:00",
                "min_employees": 1,
                "max_employees": 3
            }
        )
        overtime_shift_id = overtime_shift_response.json()["id"]
        
        # Assign employee
        client.post(
            f"/api/v1/shifts/{regular_shift_id}/assign",
            json={
                "shift_id": regular_shift_id,
                "employee_id": 1,
                "assignment_type": "regular",
                "is_overtime": False
            }
        )
        client.post(
            f"/api/v1/shifts/{overtime_shift_id}/assign",
            json={
                "shift_id": overtime_shift_id,
                "employee_id": 1,
                "assignment_type": "overtime",
                "is_overtime": True
            }
        )
        
        # Get overtime shifts
        response = client.get("/api/v1/employees/1/overtime")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1  # Only overtime shift
        assert data[0]["shift_id"] == overtime_shift_id
        assert data[0]["is_overtime"] is True
        assert data[0]["assignment_type"] == "overtime"
        assert data[0]["duration_hours"] == 4.0
    
    def test_get_overtime_with_date_filter(self, db_session, client):
        """Test filtering overtime by date range"""
        # Create schedule
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 20),
            created_by_id=1
        ))
        
        # Create availability
        avail_repo = AvailabilityRepository(db_session)
        for day in range(7):
            avail_repo.create(Availability(
                employee_id=1,
                day_of_week=day,
                start_time=time(8, 0),
                end_time=time(23, 0),
                is_recurring=True,
                is_active=True
            ))
        
        # Create overtime shifts on different dates
        ot_shift1 = client.post(
            f"/api/v1/schedules/{schedule.id}/shifts",
            json={
                "schedule_id": schedule.id,
                "date": "2026-05-12",
                "start_time": "18:00:00",
                "end_time": "22:00:00",
                "min_employees": 1,
                "max_employees": 3
            }
        )
        ot_shift2 = client.post(
            f"/api/v1/schedules/{schedule.id}/shifts",
            json={
                "schedule_id": schedule.id,
                "date": "2026-05-18",
                "start_time": "18:00:00",
                "end_time": "22:00:00",
                "min_employees": 1,
                "max_employees": 3
            }
        )
        
        # Assign employee to both
        for shift_response in [ot_shift1, ot_shift2]:
            client.post(
                f"/api/v1/shifts/{shift_response.json()['id']}/assign",
                json={
                    "shift_id": shift_response.json()["id"],
                    "employee_id": 1,
                    "assignment_type": "overtime",
                    "is_overtime": True
                }
            )
        
        # Get overtime with date filter
        response = client.get(
            "/api/v1/employees/1/overtime?start_date=2026-05-11&end_date=2026-05-15"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1  # Only first shift in range
        assert data[0]["date"] == "2026-05-12"
    
    def test_get_overtime_employee_not_found(self, db_session, client):
        """Test getting overtime for non-existent employee"""
        response = client.get("/api/v1/employees/99999/overtime")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_get_overtime_no_overtime_shifts(self, db_session, client):
        """Test getting overtime when employee has no overtime"""
        # Create schedule
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
        # Create availability
        avail_repo = AvailabilityRepository(db_session)
        avail_repo.create(Availability(
            employee_id=1,
            day_of_week=0,
            start_time=time(8, 0),
            end_time=time(18, 0),
            is_recurring=True,
            is_active=True
        ))
        
        # Create and assign only regular shift
        shift_response = client.post(
            f"/api/v1/schedules/{schedule.id}/shifts",
            json={
                "schedule_id": schedule.id,
                "date": "2026-05-12",
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "min_employees": 1,
                "max_employees": 3
            }
        )
        client.post(
            f"/api/v1/shifts/{shift_response.json()['id']}/assign",
            json={
                "shift_id": shift_response.json()["id"],
                "employee_id": 1,
                "assignment_type": "regular",
                "is_overtime": False
            }
        )
        
        # Get overtime
        response = client.get("/api/v1/employees/1/overtime")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0  # No overtime shifts

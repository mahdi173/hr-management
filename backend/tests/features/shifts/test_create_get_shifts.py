"""Unit tests for create shift and get shifts endpoints"""

import pytest
from datetime import date, time
from app.models.schedule import Schedule
from app.repositories.schedule_repository import ScheduleRepository


class TestCreateShift:
    """Tests for POST /schedules/{id}/shifts endpoint"""
    
    def test_create_shift_success(self, db_session, client):
        """Test successful shift creation"""
        # Create schedule first
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
        # Create shift
        response = client.post(
            f"/api/v1/schedules/{schedule.id}/shifts",
            json={
                "schedule_id": schedule.id,
                "date": "2026-05-12",
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "min_employees": 2,
                "max_employees": 5,
                "notes": "Morning shift"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["schedule_id"] == schedule.id
        assert data["date"] == "2026-05-12"
        assert data["min_employees"] == 2
        assert data["max_employees"] == 5
        assert "id" in data
    
    def test_create_shift_schedule_not_found(self, db_session, client):
        """Test creating shift for non-existent schedule"""
        response = client.post(
            "/api/v1/schedules/99999/shifts",
            json={
                "schedule_id": 99999,
                "date": "2026-05-12",
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "min_employees": 1,
                "max_employees": 1
            }
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_create_shift_invalid_time_order(self, db_session, client):
        """Test creating shift with end_time before start_time"""
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
        response = client.post(
            f"/api/v1/schedules/{schedule.id}/shifts",
            json={
                "schedule_id": schedule.id,
                "date": "2026-05-12",
                "start_time": "17:00:00",
                "end_time": "09:00:00",  # Invalid: before start_time
                "min_employees": 1,
                "max_employees": 1
            }
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_create_shift_date_outside_schedule_range(self, db_session, client):
        """Test creating shift with date outside schedule range"""
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
        response = client.post(
            f"/api/v1/schedules/{schedule.id}/shifts",
            json={
                "schedule_id": schedule.id,
                "date": "2026-05-20",  # Outside range
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "min_employees": 1,
                "max_employees": 1
            }
        )
        
        assert response.status_code == 400
        assert "between" in response.json()["detail"].lower()
    
    def test_create_shift_schedule_id_mismatch(self, db_session, client):
        """Test creating shift with path/body schedule_id mismatch"""
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
        response = client.post(
            f"/api/v1/schedules/{schedule.id}/shifts",
            json={
                "schedule_id": 9999,  # Different from path
                "date": "2026-05-12",
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "min_employees": 1,
                "max_employees": 1
            }
        )
        
        assert response.status_code == 400
        assert "does not match" in response.json()["detail"].lower()
    
    def test_create_shift_invalid_employee_limits(self, db_session, client):
        """Test creating shift with max_employees < min_employees"""
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
        response = client.post(
            f"/api/v1/schedules/{schedule.id}/shifts",
            json={
                "schedule_id": schedule.id,
                "date": "2026-05-12",
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "min_employees": 5,
                "max_employees": 2  # Invalid: less than min
            }
        )
        
        assert response.status_code == 422  # Validation error


class TestGetShifts:
    """Tests for GET /shifts endpoints"""
    
    def test_get_all_shifts(self, db_session, client):
        """Test getting all shifts"""
        # Create schedule and shifts
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
        # Create multiple shifts
        for i in range(3):
            client.post(
                f"/api/v1/schedules/{schedule.id}/shifts",
                json={
                    "schedule_id": schedule.id,
                    "date": f"2026-05-{12+i}",
                    "start_time": "09:00:00",
                    "end_time": "17:00:00",
                    "min_employees": 1,
                    "max_employees": 1
                }
            )
        
        # Get all shifts
        response = client.get("/api/v1/shifts")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
    
    def test_get_shifts_by_schedule(self, db_session, client):
        """Test filtering shifts by schedule"""
        # Create two schedules
        schedule_repo = ScheduleRepository(db_session)
        schedule1 = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        schedule2 = schedule_repo.create(Schedule(
            name="Week 2",
            start_date=date(2026, 5, 18),
            end_date=date(2026, 5, 24),
            created_by_id=1
        ))
        
        # Create shifts for schedule 1
        client.post(
            f"/api/v1/schedules/{schedule1.id}/shifts",
            json={
                "schedule_id": schedule1.id,
                "date": "2026-05-12",
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "min_employees": 1,
                "max_employees": 1
            }
        )
        
        # Create shift for schedule 2
        client.post(
            f"/api/v1/schedules/{schedule2.id}/shifts",
            json={
                "schedule_id": schedule2.id,
                "date": "2026-05-20",
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "min_employees": 1,
                "max_employees": 1
            }
        )
        
        # Get shifts for schedule 1
        response = client.get(f"/api/v1/shifts?schedule_id={schedule1.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["schedule_id"] == schedule1.id
    
    def test_get_shifts_by_date_range(self, db_session, client):
        """Test filtering shifts by date range"""
        # Create schedule and shifts
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 20),
            created_by_id=1
        ))
        
        # Create shifts on different dates
        for day in [12, 15, 18]:
            client.post(
                f"/api/v1/schedules/{schedule.id}/shifts",
                json={
                    "schedule_id": schedule.id,
                    "date": f"2026-05-{day}",
                    "start_time": "09:00:00",
                    "end_time": "17:00:00",
                    "min_employees": 1,
                    "max_employees": 1
                }
            )
        
        # Get shifts in range
        response = client.get(
            "/api/v1/shifts?start_date=2026-05-13&end_date=2026-05-17"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["date"] == "2026-05-15"
    
    def test_get_one_shift_success(self, db_session, client):
        """Test getting a specific shift"""
        # Create schedule and shift
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
        create_response = client.post(
            f"/api/v1/schedules/{schedule.id}/shifts",
            json={
                "schedule_id": schedule.id,
                "date": "2026-05-12",
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "min_employees": 1,
                "max_employees": 1
            }
        )
        shift_id = create_response.json()["id"]
        
        # Get shift
        response = client.get(f"/api/v1/shifts/{shift_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == shift_id
        assert data["date"] == "2026-05-12"
    
    def test_get_one_shift_not_found(self, db_session, client):
        """Test getting non-existent shift"""
        response = client.get("/api/v1/shifts/99999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_get_shifts_pagination(self, db_session, client):
        """Test pagination for shifts"""
        # Create schedule and multiple shifts
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 20),
            created_by_id=1
        ))
        
        for i in range(5):
            client.post(
                f"/api/v1/schedules/{schedule.id}/shifts",
                json={
                    "schedule_id": schedule.id,
                    "date": f"2026-05-{12+i}",
                    "start_time": "09:00:00",
                    "end_time": "17:00:00",
                    "min_employees": 1,
                    "max_employees": 1
                }
            )
        
        # Test pagination
        response = client.get(f"/api/v1/shifts?schedule_id={schedule.id}&limit=2")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

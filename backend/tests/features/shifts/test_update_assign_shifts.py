"""Unit tests for update shift, assign employee, and remove assignment endpoints"""

import pytest
from datetime import date, time
from app.models.schedule import Schedule
from app.models.availability import Availability
from app.repositories.schedule_repository import ScheduleRepository
from app.repositories.availability_repository import AvailabilityRepository


class TestUpdateShift:
    """Tests for PUT /shifts/{id} endpoint"""
    
    def test_update_shift_success(self, db_session, client):
        """Test successful shift update"""
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
                "max_employees": 3
            }
        )
        shift_id = create_response.json()["id"]
        
        # Update shift
        response = client.put(
            f"/api/v1/shifts/{shift_id}",
            json={
                "start_time": "10:00:00",
                "end_time": "18:00:00",
                "max_employees": 5
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["start_time"] == "10:00:00"
        assert data["end_time"] == "18:00:00"
        assert data["max_employees"] == 5
    
    def test_update_shift_not_found(self, db_session, client):
        """Test updating non-existent shift"""
        response = client.put(
            "/api/v1/shifts/99999",
            json={"notes": "Updated notes"}
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_update_shift_invalid_time_order(self, db_session, client):
        """Test updating shift with invalid time order"""
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
        
        # Update with invalid time
        response = client.put(
            f"/api/v1/shifts/{shift_id}",
            json={"end_time": "08:00:00"}  # Before start_time
        )
        
        assert response.status_code == 400
    
    def test_update_shift_partial(self, db_session, client):
        """Test partial shift update"""
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
                "max_employees": 3,
                "notes": "Original notes"
            }
        )
        shift_id = create_response.json()["id"]
        original_start_time = create_response.json()["start_time"]
        
        # Update only notes
        response = client.put(
            f"/api/v1/shifts/{shift_id}",
            json={"notes": "Updated notes"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["notes"] == "Updated notes"
        assert data["start_time"] == original_start_time  # Unchanged


class TestAssignEmployee:
    """Tests for POST /shifts/{id}/assign endpoint"""
    
    def test_assign_employee_success(self, db_session, client):
        """Test successful employee assignment"""
        # Create schedule and shift
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
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
        shift_id = shift_response.json()["id"]
        
        # Create availability for employee
        avail_repo = AvailabilityRepository(db_session)
        avail_repo.create(Availability(
            employee_id=1,
            day_of_week=0,  # Monday (May 12, 2026 is Monday)
            start_time=time(8, 0),
            end_time=time(18, 0),
            is_recurring=True,
            is_active=True
        ))
        
        # Assign employee
        response = client.post(
            f"/api/v1/shifts/{shift_id}/assign",
            json={
                "shift_id": shift_id,
                "employee_id": 1,
                "assignment_type": "regular",
                "is_overtime": False
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["shift_id"] == shift_id
        assert data["employee_id"] == 1
        assert data["status"] == "assigned"
    
    def test_assign_employee_shift_not_found(self, db_session, client):
        """Test assigning to non-existent shift"""
        response = client.post(
            "/api/v1/shifts/99999/assign",
            json={
                "shift_id": 99999,
                "employee_id": 1,
                "assignment_type": "regular",
                "is_overtime": False
            }
        )
        
        assert response.status_code == 404
    
    def test_assign_employee_not_available(self, db_session, client):
        """Test assigning employee who is not available"""
        # Create schedule and shift
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
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
        shift_id = shift_response.json()["id"]
        
        # Create availability that doesn't cover shift time
        avail_repo = AvailabilityRepository(db_session)
        avail_repo.create(Availability(
            employee_id=1,
            day_of_week=0,  # Monday
            start_time=time(18, 0),  # After shift
            end_time=time(22, 0),
            is_recurring=True,
            is_active=True
        ))
        
        # Try to assign
        response = client.post(
            f"/api/v1/shifts/{shift_id}/assign",
            json={
                "shift_id": shift_id,
                "employee_id": 1,
                "assignment_type": "regular",
                "is_overtime": False
            }
        )
        
        assert response.status_code == 409
        assert "not available" in response.json()["detail"].lower()
    
    def test_assign_employee_already_assigned(self, db_session, client):
        """Test assigning employee who is already assigned"""
        # Setup
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
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
        shift_id = shift_response.json()["id"]
        
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
        
        # First assignment
        client.post(
            f"/api/v1/shifts/{shift_id}/assign",
            json={
                "shift_id": shift_id,
                "employee_id": 1,
                "assignment_type": "regular",
                "is_overtime": False
            }
        )
        
        # Try to assign again
        response = client.post(
            f"/api/v1/shifts/{shift_id}/assign",
            json={
                "shift_id": shift_id,
                "employee_id": 1,
                "assignment_type": "regular",
                "is_overtime": False
            }
        )
        
        assert response.status_code == 409
        assert "already assigned" in response.json()["detail"].lower()
    
    def test_assign_employee_max_capacity_reached(self, db_session, client):
        """Test assigning when shift is at max capacity"""
        # Create schedule and shift with max 1 employee
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
        shift_response = client.post(
            f"/api/v1/schedules/{schedule.id}/shifts",
            json={
                "schedule_id": schedule.id,
                "date": "2026-05-12",
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "min_employees": 1,
                "max_employees": 1  # Max 1 employee
            }
        )
        shift_id = shift_response.json()["id"]
        
        # Create availabilities for employees
        avail_repo = AvailabilityRepository(db_session)
        for emp_id in [1, 2]:
            avail_repo.create(Availability(
                employee_id=emp_id,
                day_of_week=0,
                start_time=time(8, 0),
                end_time=time(18, 0),
                is_recurring=True,
                is_active=True
            ))
        
        # Assign first employee
        client.post(
            f"/api/v1/shifts/{shift_id}/assign",
            json={
                "shift_id": shift_id,
                "employee_id": 1,
                "assignment_type": "regular",
                "is_overtime": False
            }
        )
        
        # Try to assign second employee
        response = client.post(
            f"/api/v1/shifts/{shift_id}/assign",
            json={
                "shift_id": shift_id,
                "employee_id": 2,
                "assignment_type": "regular",
                "is_overtime": False
            }
        )
        
        assert response.status_code == 400
        assert "maximum capacity" in response.json()["detail"].lower()


class TestRemoveAssignment:
    """Tests for DELETE /shifts/{id}/assign/{employee_id} endpoint"""
    
    def test_remove_assignment_success(self, db_session, client):
        """Test successful assignment removal"""
        # Setup
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
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
        shift_id = shift_response.json()["id"]
        
        # Create availabilities and assign employees
        avail_repo = AvailabilityRepository(db_session)
        for emp_id in [1, 2]:
            avail_repo.create(Availability(
                employee_id=emp_id,
                day_of_week=0,
                start_time=time(8, 0),
                end_time=time(18, 0),
                is_recurring=True,
                is_active=True
            ))
            client.post(
                f"/api/v1/shifts/{shift_id}/assign",
                json={
                    "shift_id": shift_id,
                    "employee_id": emp_id,
                    "assignment_type": "regular",
                    "is_overtime": False
                }
            )
        
        # Remove one assignment
        response = client.delete(f"/api/v1/shifts/{shift_id}/assign/2")
        
        assert response.status_code == 200
        data = response.json()
        assert "removed" in data["message"].lower()
    
    def test_remove_assignment_not_found(self, db_session, client):
        """Test removing non-existent assignment"""
        response = client.delete("/api/v1/shifts/99999/assign/1")
        
        assert response.status_code == 404
    
    def test_remove_assignment_violates_min_employees(self, db_session, client):
        """Test removing assignment that violates min_employees"""
        # Create shift with min 2 employees
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
        shift_response = client.post(
            f"/api/v1/schedules/{schedule.id}/shifts",
            json={
                "schedule_id": schedule.id,
                "date": "2026-05-12",
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "min_employees": 2,  # Min 2
                "max_employees": 3
            }
        )
        shift_id = shift_response.json()["id"]
        
        # Assign exactly 2 employees
        avail_repo = AvailabilityRepository(db_session)
        for emp_id in [1, 2]:
            avail_repo.create(Availability(
                employee_id=emp_id,
                day_of_week=0,
                start_time=time(8, 0),
                end_time=time(18, 0),
                is_recurring=True,
                is_active=True
            ))
            client.post(
                f"/api/v1/shifts/{shift_id}/assign",
                json={
                    "shift_id": shift_id,
                    "employee_id": emp_id,
                    "assignment_type": "regular",
                    "is_overtime": False
                }
            )
        
        # Try to remove one (would violate min_employees)
        response = client.delete(f"/api/v1/shifts/{shift_id}/assign/1")
        
        assert response.status_code == 400
        assert "minimum" in response.json()["detail"].lower()

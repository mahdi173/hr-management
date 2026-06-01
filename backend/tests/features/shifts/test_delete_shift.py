"""Unit tests for delete shift endpoint"""

import pytest
from datetime import date
from app.models.schedule import Schedule
from app.repositories.schedule_repository import ScheduleRepository


class TestDeleteShift:
    """Tests for DELETE /shifts/{shift_id} endpoint"""
    
    def test_delete_shift_success(self, db_session, client):
        """Test successful shift deletion"""
        # Create schedule first
        schedule_repo = ScheduleRepository(db_session)
        schedule = schedule_repo.create(Schedule(
            name="Week 1",
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 17),
            created_by_id=1
        ))
        
        # Create shift
        create_response = client.post(
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
        assert create_response.status_code == 201
        shift_id = create_response.json()["id"]
        
        # Delete shift
        delete_response = client.delete(f"/api/v1/shifts/{shift_id}")
        assert delete_response.status_code == 204
        
        # Verify it's gone
        get_response = client.get(f"/api/v1/shifts/{shift_id}")
        assert get_response.status_code == 404

    def test_delete_shift_not_found(self, db_session, client):
        """Test deleting a non-existent shift"""
        response = client.delete("/api/v1/shifts/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

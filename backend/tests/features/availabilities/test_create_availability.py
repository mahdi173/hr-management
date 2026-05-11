import pytest
from fastapi import status
from datetime import date


def test_create_recurring_availability_success(client):
    """Test successful creation of a recurring availability"""
    # First, create an employee
    employee_res = client.post(
        "/employees",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com",
            "phone": "+33612345678",
            "role_id": 1,
            "contract_type_id": 1
        }
    )
    employee_id = employee_res.json()["id"]
    
    # Create recurring availability
    response = client.post(
        f"/employees/{employee_id}/availabilities",
        json={
            "employee_id": employee_id,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "day_of_week": 0,  # Monday
            "is_recurring": True,
            "is_active": True
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["employee_id"] == employee_id
    assert data["day_of_week"] == 0
    assert data["is_recurring"] is True
    assert data["specific_date"] is None
    assert "id" in data


def test_create_specific_date_availability_success(client):
    """Test successful creation of a specific date availability"""
    # Create employee
    employee_res = client.post(
        "/employees",
        json={
            "first_name": "Test",
            "last_name": "User2",
            "email": "test.user2@example.com",
            "phone": "+33612345679",
            "role_id": 1,
            "contract_type_id": 1
        }
    )
    employee_id = employee_res.json()["id"]
    
    # Create specific date availability
    response = client.post(
        f"/employees/{employee_id}/availabilities",
        json={
            "employee_id": employee_id,
            "start_time": "10:00:00",
            "end_time": "14:00:00",
            "is_recurring": False,
            "specific_date": "2026-06-15",
            "is_active": True
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["is_recurring"] is False
    assert data["specific_date"] == "2026-06-15"
    assert data["day_of_week"] is None


def test_create_availability_employee_not_found(client):
    """Test that creating availability for non-existent employee fails"""
    response = client.post(
        "/employees/99999/availabilities",
        json={
            "employee_id": 99999,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "day_of_week": 0,
            "is_recurring": True
        }
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()


def test_create_availability_overlapping(client):
    """Test that overlapping availabilities are rejected"""
    # Create employee
    employee_res = client.post(
        "/employees",
        json={
            "first_name": "Test",
            "last_name": "User3",
            "email": "test.user3@example.com",
            "phone": "+33612345680",
            "role_id": 1,
            "contract_type_id": 1
        }
    )
    employee_id = employee_res.json()["id"]
    
    # Create first availability (Monday 9-17)
    client.post(
        f"/employees/{employee_id}/availabilities",
        json={
            "employee_id": employee_id,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "day_of_week": 0,
            "is_recurring": True
        }
    )
    
    # Try to create overlapping availability (Monday 10-12)
    response = client.post(
        f"/employees/{employee_id}/availabilities",
        json={
            "employee_id": employee_id,
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "day_of_week": 0,
            "is_recurring": True
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "overlaps" in response.json()["detail"].lower()


def test_create_availability_invalid_time_order(client):
    """Test that end_time must be after start_time"""
    # Create employee
    employee_res = client.post(
        "/employees",
        json={
            "first_name": "Test",
            "last_name": "User4",
            "email": "test.user4@example.com",
            "phone": "+33612345681",
            "role_id": 1,
            "contract_type_id": 1
        }
    )
    employee_id = employee_res.json()["id"]
    
    # Try to create availability with end_time before start_time
    response = client.post(
        f"/employees/{employee_id}/availabilities",
        json={
            "employee_id": employee_id,
            "start_time": "17:00:00",
            "end_time": "09:00:00",
            "day_of_week": 0,
            "is_recurring": True
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_availability_missing_day_of_week_for_recurring(client):
    """Test that day_of_week is required for recurring availability"""
    # Create employee
    employee_res = client.post(
        "/employees",
        json={
            "first_name": "Test",
            "last_name": "User5",
            "email": "test.user5@example.com",
            "phone": "+33612345682",
            "role_id": 1,
            "contract_type_id": 1
        }
    )
    employee_id = employee_res.json()["id"]
    
    # Try to create recurring availability without day_of_week
    response = client.post(
        f"/employees/{employee_id}/availabilities",
        json={
            "employee_id": employee_id,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "is_recurring": True
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_availability_missing_specific_date_for_non_recurring(client):
    """Test that specific_date is required for non-recurring availability"""
    # Create employee
    employee_res = client.post(
        "/employees",
        json={
            "first_name": "Test",
            "last_name": "User6",
            "email": "test.user6@example.com",
            "phone": "+33612345683",
            "role_id": 1,
            "contract_type_id": 1
        }
    )
    employee_id = employee_res.json()["id"]
    
    # Try to create non-recurring availability without specific_date
    response = client.post(
        f"/employees/{employee_id}/availabilities",
        json={
            "employee_id": employee_id,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "is_recurring": False
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_availability_employee_id_mismatch(client):
    """Test that employee_id in path must match employee_id in body"""
    response = client.post(
        "/employees/1/availabilities",
        json={
            "employee_id": 999,  # Different from path
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "day_of_week": 0,
            "is_recurring": True
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "must match" in response.json()["detail"].lower()

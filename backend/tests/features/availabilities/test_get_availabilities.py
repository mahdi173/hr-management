import pytest
from fastapi import status


def test_get_employee_availabilities(client):
    """Test retrieving all availabilities for an employee"""
    # Create employee
    employee_res = client.post(
        "/employees",
        json={
            "first_name": "Test",
            "last_name": "GetUser",
            "email": "test.getuser@example.com",
            "phone": "+33612345690",
            "role_id": 1,
            "contract_type_id": 1
        }
    )
    employee_id = employee_res.json()["id"]
    
    # Create multiple availabilities
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
    client.post(
        f"/employees/{employee_id}/availabilities",
        json={
            "employee_id": employee_id,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "day_of_week": 1,
            "is_recurring": True
        }
    )
    
    # Get all availabilities
    response = client.get(f"/employees/{employee_id}/availabilities")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2
    assert isinstance(data, list)


def test_get_employee_availabilities_active_only(client):
    """Test filtering availabilities by active status"""
    # Create employee
    employee_res = client.post(
        "/employees",
        json={
            "first_name": "Test",
            "last_name": "ActiveUser",
            "email": "test.activeuser@example.com",
            "phone": "+33612345691",
            "role_id": 1,
            "contract_type_id": 1
        }
    )
    employee_id = employee_res.json()["id"]
    
    # Create active availability
    active_res = client.post(
        f"/employees/{employee_id}/availabilities",
        json={
            "employee_id": employee_id,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "day_of_week": 0,
            "is_recurring": True,
            "is_active": True
        }
    )
    
    # Create and then deactivate another availability
    inactive_res = client.post(
        f"/employees/{employee_id}/availabilities",
        json={
            "employee_id": employee_id,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "day_of_week": 1,
            "is_recurring": True,
            "is_active": True
        }
    )
    inactive_id = inactive_res.json()["id"]
    client.delete(f"/availabilities/{inactive_id}")  # Soft delete
    
    # Get only active availabilities
    response = client.get(f"/employees/{employee_id}/availabilities?active_only=true")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(av["is_active"] is True for av in data)
    
    # Get all availabilities including inactive
    response = client.get(f"/employees/{employee_id}/availabilities?active_only=false")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2


def test_get_employee_availabilities_employee_not_found(client):
    """Test getting availabilities for non-existent employee"""
    response = client.get("/employees/99999/availabilities")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_one_availability_success(client):
    """Test retrieving a single availability by ID"""
    # Create employee and availability
    employee_res = client.post(
        "/employees",
        json={
            "first_name": "Test",
            "last_name": "OneUser",
            "email": "test.oneuser@example.com",
            "phone": "+33612345692",
            "role_id": 1,
            "contract_type_id": 1
        }
    )
    employee_id = employee_res.json()["id"]
    
    create_res = client.post(
        f"/employees/{employee_id}/availabilities",
        json={
            "employee_id": employee_id,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "day_of_week": 2,
            "is_recurring": True
        }
    )
    availability_id = create_res.json()["id"]
    
    # Get specific availability
    response = client.get(f"/availabilities/{availability_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == availability_id
    assert data["day_of_week"] == 2


def test_get_one_availability_not_found(client):
    """Test retrieving a non-existent availability"""
    response = client.get("/availabilities/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()


def test_get_empty_availabilities_list(client):
    """Test getting availabilities when none exist for employee"""
    # Create employee without availabilities
    employee_res = client.post(
        "/employees",
        json={
            "first_name": "Test",
            "last_name": "EmptyUser",
            "email": "test.emptyuser@example.com",
            "phone": "+33612345693",
            "role_id": 1,
            "contract_type_id": 1
        }
    )
    employee_id = employee_res.json()["id"]
    
    response = client.get(f"/employees/{employee_id}/availabilities")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

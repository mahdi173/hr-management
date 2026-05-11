import pytest
from fastapi import status


def test_update_availability_success(client):
    """Test successful update of an availability"""
    # Create employee and availability
    employee_res = client.post(
        "/employees",
        json={
            "first_name": "Test",
            "last_name": "UpdateUser",
            "email": "test.updateuser@example.com",
            "phone": "+33612345694",
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
            "day_of_week": 0,
            "is_recurring": True
        }
    )
    availability_id = create_res.json()["id"]
    
    # Update end_time
    response = client.put(
        f"/availabilities/{availability_id}",
        json={"end_time": "16:00:00"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["end_time"] == "16:00:00"
    assert data["start_time"] == "09:00:00"  # Unchanged


def test_update_availability_partial(client):
    """Test partial update of an availability"""
    # Create employee and availability
    employee_res = client.post(
        "/employees",
        json={
            "first_name": "Test",
            "last_name": "PartialUser",
            "email": "test.partialuser@example.com",
            "phone": "+33612345695",
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
            "day_of_week": 0,
            "is_recurring": True,
            "is_active": True
        }
    )
    availability_id = create_res.json()["id"]
    
    # Update only is_active
    response = client.put(
        f"/availabilities/{availability_id}",
        json={"is_active": False}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_active"] is False
    assert data["start_time"] == "09:00:00"
    assert data["end_time"] == "17:00:00"


def test_update_availability_not_found(client):
    """Test updating a non-existent availability"""
    response = client.put(
        "/availabilities/99999",
        json={"end_time": "16:00:00"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_availability_with_overlap(client):
    """Test that updating to overlapping times is rejected"""
    # Create employee
    employee_res = client.post(
        "/employees",
        json={
            "first_name": "Test",
            "last_name": "OverlapUser",
            "email": "test.overlapuser@example.com",
            "phone": "+33612345696",
            "role_id": 1,
            "contract_type_id": 1
        }
    )
    employee_id = employee_res.json()["id"]
    
    # Create two availabilities on Monday
    client.post(
        f"/employees/{employee_id}/availabilities",
        json={
            "employee_id": employee_id,
            "start_time": "09:00:00",
            "end_time": "12:00:00",
            "day_of_week": 0,
            "is_recurring": True
        }
    )
    
    create_res2 = client.post(
        f"/employees/{employee_id}/availabilities",
        json={
            "employee_id": employee_id,
            "start_time": "14:00:00",
            "end_time": "17:00:00",
            "day_of_week": 0,
            "is_recurring": True
        }
    )
    availability_id = create_res2.json()["id"]
    
    # Try to update to overlap with first availability
    response = client.put(
        f"/availabilities/{availability_id}",
        json={"start_time": "11:00:00"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "overlaps" in response.json()["detail"].lower()


def test_update_availability_invalid_time_order(client):
    """Test that updated end_time must still be after start_time"""
    # Create employee and availability
    employee_res = client.post(
        "/employees",
        json={
            "first_name": "Test",
            "last_name": "TimeUser",
            "email": "test.timeuser@example.com",
            "phone": "+33612345697",
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
            "day_of_week": 0,
            "is_recurring": True
        }
    )
    availability_id = create_res.json()["id"]
    
    # Try to update with invalid time order
    response = client.put(
        f"/availabilities/{availability_id}",
        json={"start_time": "18:00:00", "end_time": "17:00:00"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_availability_soft_delete(client):
    """Test soft delete (deactivate) of an availability"""
    # Create employee and availability
    employee_res = client.post(
        "/employees",
        json={
            "first_name": "Test",
            "last_name": "DeleteUser",
            "email": "test.deleteuser@example.com",
            "phone": "+33612345698",
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
            "day_of_week": 0,
            "is_recurring": True
        }
    )
    availability_id = create_res.json()["id"]
    
    # Soft delete
    response = client.delete(f"/availabilities/{availability_id}")
    assert response.status_code == status.HTTP_200_OK
    assert "deactivated" in response.json()["message"].lower()
    
    # Verify it's deactivated
    get_response = client.get(f"/availabilities/{availability_id}")
    assert get_response.json()["is_active"] is False


def test_delete_availability_hard_delete(client):
    """Test hard delete (permanent removal) of an availability"""
    # Create employee and availability
    employee_res = client.post(
        "/employees",
        json={
            "first_name": "Test",
            "last_name": "HardDeleteUser",
            "email": "test.harddeleteuser@example.com",
            "phone": "+33612345699",
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
            "day_of_week": 0,
            "is_recurring": True
        }
    )
    availability_id = create_res.json()["id"]
    
    # Hard delete
    response = client.delete(f"/availabilities/{availability_id}?hard_delete=true")
    assert response.status_code == status.HTTP_200_OK
    assert "permanently deleted" in response.json()["message"].lower()
    
    # Verify it's gone
    get_response = client.get(f"/availabilities/{availability_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_availability_not_found(client):
    """Test deleting a non-existent availability"""
    response = client.delete("/availabilities/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

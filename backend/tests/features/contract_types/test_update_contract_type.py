import pytest
from fastapi import status


def test_update_contract_type_success(client):
    """Test successful update of a contract type"""
    create_res = client.post(
        "/contract-types/",
        json={"name": "Original Name", "weekly_hours": 35.0}
    )
    contract_id = create_res.json()["id"]
    
    response = client.put(
        f"/contract-types/{contract_id}",
        json={
            "name": "Updated Name",
            "description": "New Description",
            "weekly_hours": 40.0
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["description"] == "New Description"
    assert data["weekly_hours"] == 40.0


def test_update_contract_type_partial(client):
    """Test partial update (only some fields)"""
    create_res = client.post(
        "/contract-types/",
        json={
            "name": "Original",
            "description": "Original Desc",
            "weekly_hours": 35.0,
            "max_weekly_hours": 48.0
        }
    )
    contract_id = create_res.json()["id"]
    
    # Update only description
    response = client.put(
        f"/contract-types/{contract_id}",
        json={"description": "Updated Description"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Original"  # Unchanged
    assert data["description"] == "Updated Description"  # Changed
    assert data["weekly_hours"] == 35.0  # Unchanged


def test_update_contract_type_duplicate_name(client):
    """Test that updating to an existing name is rejected"""
    client.post(
        "/contract-types/",
        json={"name": "Existing Contract", "weekly_hours": 35.0}
    )
    create_res = client.post(
        "/contract-types/",
        json={"name": "To Update", "weekly_hours": 35.0}
    )
    contract_id = create_res.json()["id"]
    
    response = client.put(
        f"/contract-types/{contract_id}",
        json={"name": "Existing Contract"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]


def test_update_contract_type_not_found(client):
    """Test updating a non-existent contract type"""
    response = client.put(
        "/contract-types/99999",
        json={"name": "New Name"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"]


def test_update_contract_type_invalid_max_hours(client):
    """Test that max_weekly_hours validation works on update"""
    create_res = client.post(
        "/contract-types/",
        json={"name": "Test Contract", "weekly_hours": 35.0}
    )
    contract_id = create_res.json()["id"]
    
    # Try to set max_weekly_hours less than weekly_hours
    response = client.put(
        f"/contract-types/{contract_id}",
        json={"max_weekly_hours": 20.0}  # Less than 35.0
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "max_weekly_hours must be greater than or equal to weekly_hours" in response.json()["detail"]


def test_update_contract_type_hours_validation(client):
    """Test that updating weekly_hours validates against max_weekly_hours"""
    create_res = client.post(
        "/contract-types/",
        json={
            "name": "Test Contract",
            "weekly_hours": 35.0,
            "max_weekly_hours": 40.0
        }
    )
    contract_id = create_res.json()["id"]
    
    # Try to set weekly_hours greater than max_weekly_hours
    response = client.put(
        f"/contract-types/{contract_id}",
        json={"weekly_hours": 45.0}  # Greater than max 40.0
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_contract_type_deactivate(client):
    """Test deactivating a contract type"""
    create_res = client.post(
        "/contract-types/",
        json={"name": "Active Contract", "weekly_hours": 35.0}
    )
    contract_id = create_res.json()["id"]
    
    response = client.put(
        f"/contract-types/{contract_id}",
        json={"is_active": False}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_active"] is False


def test_update_contract_type_same_name(client):
    """Test that updating a contract type with its own name is allowed"""
    create_res = client.post(
        "/contract-types/",
        json={"name": "Contract Name", "weekly_hours": 35.0}
    )
    contract_id = create_res.json()["id"]
    
    # Update with same name but different description
    response = client.put(
        f"/contract-types/{contract_id}",
        json={"name": "Contract Name", "description": "New Description"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Contract Name"
    assert data["description"] == "New Description"

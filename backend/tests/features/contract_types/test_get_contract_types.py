import pytest
from fastapi import status


def test_get_all_contract_types(client):
    """Test retrieving all contract types"""
    # Create some contract types
    client.post(
        "/contract-types/",
        json={"name": "Contract Type 1", "weekly_hours": 35.0}
    )
    client.post(
        "/contract-types/",
        json={"name": "Contract Type 2", "weekly_hours": 20.0}
    )
    
    response = client.get("/contract-types/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2
    assert isinstance(data, list)


def test_get_all_contract_types_with_pagination(client):
    """Test pagination parameters"""
    # Create multiple contract types
    for i in range(5):
        client.post(
            "/contract-types/",
            json={"name": f"Contract {i}", "weekly_hours": 35.0}
        )
    
    # Test with limit
    response = client.get("/contract-types/?limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) <= 2
    
    # Test with skip
    response = client.get("/contract-types/?skip=2&limit=3")
    assert response.status_code == status.HTTP_200_OK


def test_get_all_contract_types_active_only(client):
    """Test filtering by active status"""
    # Create active contract type
    client.post(
        "/contract-types/",
        json={"name": "Active Contract", "weekly_hours": 35.0, "is_active": True}
    )
    
    # Create inactive contract type
    create_res = client.post(
        "/contract-types/",
        json={"name": "Inactive Contract", "weekly_hours": 35.0, "is_active": True}
    )
    contract_id = create_res.json()["id"]
    
    # Deactivate it
    client.put(
        f"/contract-types/{contract_id}",
        json={"is_active": False}
    )
    
    # Get only active
    response = client.get("/contract-types/?active_only=true")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    for contract_type in data:
        assert contract_type["is_active"] is True


def test_get_one_contract_type_success(client):
    """Test retrieving a single contract type by ID"""
    create_res = client.post(
        "/contract-types/",
        json={
            "name": "Single Contract",
            "description": "Test description",
            "weekly_hours": 35.0
        }
    )
    contract_id = create_res.json()["id"]
    
    response = client.get(f"/contract-types/{contract_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Single Contract"
    assert data["description"] == "Test description"
    assert data["id"] == contract_id


def test_get_one_contract_type_not_found(client):
    """Test retrieving a non-existent contract type"""
    response = client.get("/contract-types/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"]


def test_get_empty_contract_types_list(client):
    """Test getting contract types when none exist"""
    # Don't create any contract types
    response = client.get("/contract-types/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)

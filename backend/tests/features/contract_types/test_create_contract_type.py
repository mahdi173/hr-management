import pytest
from fastapi import status


def test_create_contract_type_success(client):
    """Test successful creation of a contract type"""
    response = client.post(
        "/contract-types/",
        json={
            "name": "New Contract Type",
            "description": "New contract description",
            "weekly_hours": 35.0,
            "max_weekly_hours": 40.0,
            "is_active": True
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "New Contract Type"
    assert data["weekly_hours"] == 35.0
    assert data["max_weekly_hours"] == 40.0
    assert "id" in data


def test_create_contract_type_duplicate_name(client):
    """Test that duplicate contract type names are rejected"""
    # First creation
    client.post(
        "/contract-types/",
        json={"name": "Duplicate", "weekly_hours": 35.0}
    )
    
    # Second creation with same name
    response = client.post(
        "/contract-types/",
        json={"name": "Duplicate", "weekly_hours": 35.0}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]


def test_create_contract_type_invalid_weekly_hours(client):
    """Test that invalid weekly hours are rejected"""
    # Weekly hours too low (must be > 0)
    response = client.post(
        "/contract-types/",
        json={"name": "Invalid Hours", "weekly_hours": 0}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Weekly hours too high (must be <= 168)
    response = client.post(
        "/contract-types/",
        json={"name": "Invalid Hours", "weekly_hours": 200}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_contract_type_max_hours_less_than_weekly(client):
    """Test that max_weekly_hours must be >= weekly_hours"""
    response = client.post(
        "/contract-types/",
        json={
            "name": "Invalid Max Hours",
            "weekly_hours": 35.0,
            "max_weekly_hours": 20.0  # Less than weekly_hours
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "max_weekly_hours must be greater than or equal to weekly_hours" in response.json()["detail"]


def test_create_contract_type_missing_required_fields(client):
    """Test that required fields are validated"""
    # Missing name
    response = client.post(
        "/contract-types/",
        json={"weekly_hours": 35.0}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Missing weekly_hours
    response = client.post(
        "/contract-types/",
        json={"name": "Test"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_contract_type_with_optional_fields(client):
    """Test creation with only required fields (description and max_weekly_hours are optional)"""
    response = client.post(
        "/contract-types/",
        json={
            "name": "Minimal Contract",
            "weekly_hours": 35.0
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Minimal Contract"
    assert data["weekly_hours"] == 35.0
    assert data["is_active"] is True  # Default value

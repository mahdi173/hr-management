import pytest
from fastapi import status

def test_create_role_success(client):
    response = client.post(
        "/roles/",
        json={"name": "New Role", "description": "New Description"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "New Role"
    assert "id" in data

def test_create_role_duplicate_name(client):
    # First creation
    client.post("/roles/", json={"name": "Duplicate"})
    
    # Second creation
    response = client.post("/roles/", json={"name": "Duplicate"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]

def test_create_role_invalid_data(client):
    response = client.post("/roles/", json={"name": ""})  # Name too short
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

import pytest
from fastapi import status

def test_update_role_success(client):
    create_res = client.post("/roles/", json={"name": "Original Name"})
    role_id = create_res.json()["id"]
    
    response = client.put(
        f"/roles/{role_id}",
        json={"name": "Updated Name", "description": "New Desc"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["description"] == "New Desc"

def test_update_role_duplicate_name(client):
    client.post("/roles/", json={"name": "Existing"})
    create_res = client.post("/roles/", json={"name": "To Update"})
    role_id = create_res.json()["id"]
    
    response = client.put(
        f"/roles/{role_id}",
        json={"name": "Existing"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_update_role_not_found(client):
    response = client.put("/roles/9999", json={"name": "New"})
    assert response.status_code == status.HTTP_404_NOT_FOUND

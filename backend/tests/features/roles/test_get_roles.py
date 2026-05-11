import pytest
from fastapi import status

def test_get_all_roles(client):
    # Create some roles
    client.post("/roles/", json={"name": "Role 1"})
    client.post("/roles/", json={"name": "Role 2"})
    
    response = client.get("/roles/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2

def test_get_one_role_success(client):
    create_res = client.post("/roles/", json={"name": "Single Role"})
    role_id = create_res.json()["id"]
    
    response = client.get(f"/roles/{role_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Single Role"

def test_get_one_role_not_found(client):
    response = client.get("/roles/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

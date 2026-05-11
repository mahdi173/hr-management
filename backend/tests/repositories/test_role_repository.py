import pytest
from app.repositories.role_repository import RoleRepository
from app.models.role import Role

def test_create_role(db_session):
    repo = RoleRepository(db_session)
    role_data = {"name": "Test Role", "description": "Test Description"}
    role = repo.create(role_data)
    
    assert role.id is not None
    assert role.name == "Test Role"
    assert role.description == "Test Description"

def test_get_by_name(db_session):
    repo = RoleRepository(db_session)
    role_name = "Unique Role"
    repo.create({"name": role_name})
    
    role = repo.get_by_name(role_name)
    assert role is not None
    assert role.name == role_name

def test_name_exists(db_session):
    repo = RoleRepository(db_session)
    role_name = "Existing Role"
    repo.create({"name": role_name})
    
    assert repo.name_exists(role_name) is True
    assert repo.name_exists("Non Existing") is False

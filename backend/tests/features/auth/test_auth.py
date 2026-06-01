"""Authentication integration tests."""

import pytest
from fastapi import status

from app.core.security import hash_password
from app.models.employee import Employee
from app.models.role import Role
from app.models.user import User


def _link_user(db_session, email: str, password: str, employee: Employee):
    user = User(
        email=email,
        hashed_password=hash_password(password),
        is_active=True,
        employee_id=employee.id,
    )
    db_session.add(user)
    db_session.commit()
    return user


def test_login_and_me(anonymous_client, db_session):
    client = anonymous_client
    role = db_session.query(Role).filter(Role.name == "Employee").first()
    emp = Employee(
        first_name="Auth",
        last_name="User",
        email="auth.user@example.com",
        role_id=role.id,
        contract_type_id=1,
        is_active=True,
    )
    db_session.add(emp)
    db_session.commit()
    _link_user(db_session, "auth@test.com", "secret123", emp)

    login = client.post(
        "/auth/login",
        json={"email": "auth@test.com", "password": "secret123"},
    )
    assert login.status_code == status.HTTP_200_OK
    assert login.json()["email"] == "auth@test.com"
    assert "access_token" in login.cookies

    me = client.get("/auth/me")
    assert me.status_code == status.HTTP_200_OK
    assert me.json()["employee_id"] == emp.id


def test_login_invalid_credentials(anonymous_client, db_session):
    client = anonymous_client
    response = client.post(
        "/auth/login",
        json={"email": "nobody@test.com", "password": "wrong"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_me_requires_auth(anonymous_client):
    client = anonymous_client
    response = client.get("/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout_clears_session(anonymous_client, db_session):
    client = anonymous_client
    role = db_session.query(Role).filter(Role.name == "Manager").first()
    emp = Employee(
        first_name="Mgr",
        last_name="Out",
        email="logout.mgr@example.com",
        role_id=role.id,
        contract_type_id=1,
        is_active=True,
    )
    db_session.add(emp)
    db_session.commit()
    _link_user(db_session, "logout@test.com", "pass123", emp)

    client.post("/auth/login", json={"email": "logout@test.com", "password": "pass123"})
    assert client.get("/auth/me").status_code == status.HTTP_200_OK

    client.post("/auth/logout")
    assert client.get("/auth/me").status_code == status.HTTP_401_UNAUTHORIZED


def test_protected_route_requires_auth(anonymous_client):
    client = anonymous_client
    response = client.get("/employees/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

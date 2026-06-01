import os

# Use in-memory SQLite before app modules load the default Postgres URL
os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import get_db
from app.models import Base
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def _seed_base_data(session):
    from app.models.role import Role
    from app.models.contract_type import ContractType
    from app.models.employee import Employee

    if not session.query(Role).filter(Role.name == "Admin").first():
        session.add(Role(id=1, name="Admin", is_active=True))
    if not session.query(Role).filter(Role.name == "Manager").first():
        session.add(Role(id=2, name="Manager", is_active=True))
    if not session.query(Role).filter(Role.name == "Employee").first():
        session.add(Role(id=3, name="Employee", is_active=True))
    session.commit()

    if not session.query(ContractType).filter(ContractType.id == 1).first():
        session.add(ContractType(id=1, name="CDI", weekly_hours=35.0, is_active=True))
        session.commit()

    if not session.query(Employee).filter(Employee.id == 1).first():
        session.add(
            Employee(
                id=1,
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                role_id=3,
                contract_type_id=1,
                is_active=True,
            )
        )
    if not session.query(Employee).filter(Employee.id == 2).first():
        session.add(
            Employee(
                id=2,
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@example.com",
                role_id=2,
                contract_type_id=1,
                is_active=True,
            )
        )
    session.commit()


def _create_user(session, email: str, password: str, employee_id: int, role_name: str):
    from app.models.user import User
    from app.core.security import hash_password

    existing = session.query(User).filter(User.email == email).first()
    if existing:
        return existing

    user = User(
        email=email,
        hashed_password=hash_password(password),
        is_active=True,
        employee_id=employee_id,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    _seed_base_data(session)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def anonymous_client(db_session):
    """API client without authentication (for auth flow tests)."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def client(db_session, anonymous_client):
    """API client logged in as manager (default for existing integration tests)."""
    from app.models.employee import Employee

    mgr = db_session.query(Employee).filter(Employee.id == 2).first()
    _create_user(db_session, "manager@test.com", "manager123", mgr.id, "Manager")
    anonymous_client.post(
        "/auth/login",
        json={"email": "manager@test.com", "password": "manager123"},
    )
    return anonymous_client


@pytest.fixture
def auth_manager(client, db_session):
    """Client authenticated as a manager."""
    from app.models.employee import Employee

    mgr = db_session.query(Employee).filter(Employee.id == 2).first()
    _create_user(db_session, "manager@test.com", "manager123", mgr.id, "Manager")
    client.post("/auth/login", json={"email": "manager@test.com", "password": "manager123"})
    return client


@pytest.fixture
def auth_employee(client, db_session):
    """Client authenticated as a regular employee."""
    from app.models.employee import Employee

    emp = db_session.query(Employee).filter(Employee.id == 1).first()
    _create_user(db_session, "employee@test.com", "employee123", emp.id, "Employee")
    client.post("/auth/login", json={"email": "employee@test.com", "password": "employee123"})
    return client

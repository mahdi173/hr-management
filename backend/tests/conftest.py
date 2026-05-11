import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import get_db
from app.models import Base
from app.main import app

# Use SQLite in-memory for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create tables once for the entire test session"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Get a fresh database session for each test"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    # Seed roles and contract types for tests
    from app.models.role import Role
    from app.models.contract_type import ContractType
    
    # Create roles if they don't exist
    if not session.query(Role).filter(Role.id == 1).first():
        session.add(Role(id=1, name="Manager", is_active=True))
        session.add(Role(id=2, name="Employee", is_active=True))
        session.commit()
    
    # Create contract types if they don't exist
    if not session.query(ContractType).filter(ContractType.id == 1).first():
        session.add(ContractType(id=1, name="CDI", weekly_hours=35.0, is_active=True))
        session.add(ContractType(id=2, name="CDD", weekly_hours=35.0, is_active=True))
        session.commit()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Get a test client with a mocked database session"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

import pytest
from app.repositories.contract_type_repository import ContractTypeRepository
from app.models.contract_type import ContractType


def test_create_contract_type(db_session):
    """Test creating a contract type via repository"""
    repo = ContractTypeRepository(db_session)
    contract_data = {
        "name": "Test Contract",
        "description": "Test Description",
        "weekly_hours": 35.0,
        "max_weekly_hours": 48.0,
        "is_active": True
    }
    contract_type = repo.create(contract_data)
    
    assert contract_type.id is not None
    assert contract_type.name == "Test Contract"
    assert contract_type.description == "Test Description"
    assert contract_type.weekly_hours == 35.0
    assert contract_type.max_weekly_hours == 48.0
    assert contract_type.is_active is True


def test_get_by_name(db_session):
    """Test retrieving a contract type by name"""
    repo = ContractTypeRepository(db_session)
    contract_name = "Unique Contract"
    repo.create({"name": contract_name, "weekly_hours": 35.0})
    
    contract_type = repo.get_by_name(contract_name)
    assert contract_type is not None
    assert contract_type.name == contract_name


def test_get_by_name_not_found(db_session):
    """Test that get_by_name returns None for non-existent name"""
    repo = ContractTypeRepository(db_session)
    
    contract_type = repo.get_by_name("Non Existent")
    assert contract_type is None


def test_name_exists(db_session):
    """Test checking if a contract type name exists"""
    repo = ContractTypeRepository(db_session)
    contract_name = "Existing Contract"
    repo.create({"name": contract_name, "weekly_hours": 35.0})
    
    assert repo.name_exists(contract_name) is True
    assert repo.name_exists("Non Existing") is False


def test_name_exists_exclude_id(db_session):
    """Test name_exists with exclude_id parameter"""
    repo = ContractTypeRepository(db_session)
    
    # Create two contract types
    contract1 = repo.create({"name": "Contract 1", "weekly_hours": 35.0})
    repo.create({"name": "Contract 2", "weekly_hours": 35.0})
    
    # Check if "Contract 1" exists excluding its own ID (should return False)
    assert repo.name_exists("Contract 1", exclude_id=contract1.id) is False
    
    # Check if "Contract 2" exists excluding contract1's ID (should return True)
    assert repo.name_exists("Contract 2", exclude_id=contract1.id) is True


def test_get_active_contract_types(db_session):
    """Test retrieving only active contract types"""
    repo = ContractTypeRepository(db_session)
    
    # Create active contract types
    repo.create({"name": "Active 1", "weekly_hours": 35.0, "is_active": True})
    repo.create({"name": "Active 2", "weekly_hours": 35.0, "is_active": True})
    
    # Create inactive contract type
    repo.create({"name": "Inactive", "weekly_hours": 35.0, "is_active": False})
    
    active_contracts = repo.get_active_contract_types()
    assert len(active_contracts) >= 2
    for contract in active_contracts:
        assert contract.is_active is True


def test_get_active_contract_types_pagination(db_session):
    """Test pagination in get_active_contract_types"""
    repo = ContractTypeRepository(db_session)
    
    # Create multiple active contract types
    for i in range(5):
        repo.create({"name": f"Active {i}", "weekly_hours": 35.0, "is_active": True})
    
    # Test with limit
    contracts = repo.get_active_contract_types(skip=0, limit=2)
    assert len(contracts) == 2
    
    # Test with skip
    contracts = repo.get_active_contract_types(skip=2, limit=2)
    assert len(contracts) >= 2


def test_get_all_contract_types(db_session):
    """Test retrieving all contract types (active and inactive)"""
    repo = ContractTypeRepository(db_session)
    
    # Create active and inactive contract types
    repo.create({"name": "Active", "weekly_hours": 35.0, "is_active": True})
    repo.create({"name": "Inactive", "weekly_hours": 35.0, "is_active": False})
    
    all_contracts = repo.get_all()
    assert len(all_contracts) >= 2


def test_get_by_id(db_session):
    """Test retrieving a contract type by ID"""
    repo = ContractTypeRepository(db_session)
    
    created = repo.create({"name": "Test Contract", "weekly_hours": 35.0})
    
    retrieved = repo.get_by_id(created.id)
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.name == "Test Contract"


def test_update_contract_type(db_session):
    """Test updating a contract type"""
    repo = ContractTypeRepository(db_session)
    
    # Create a contract type
    contract = repo.create({"name": "Original", "weekly_hours": 35.0})
    
    # Update it
    updated = repo.update(
        contract.id,
        {"name": "Updated", "description": "New Description"}
    )
    
    assert updated.name == "Updated"
    assert updated.description == "New Description"
    assert updated.weekly_hours == 35.0  # Unchanged


def test_delete_contract_type(db_session):
    """Test deleting a contract type"""
    repo = ContractTypeRepository(db_session)
    
    # Create a contract type
    contract = repo.create({"name": "To Delete", "weekly_hours": 35.0})
    contract_id = contract.id
    
    # Delete it
    repo.delete(contract_id)
    
    # Verify it's deleted
    retrieved = repo.get_by_id(contract_id)
    assert retrieved is None

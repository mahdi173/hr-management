import pytest
from datetime import time, date
from app.repositories.availability_repository import AvailabilityRepository
from app.repositories.employee_repository import EmployeeRepository
from app.models.availability import Availability


def test_create_availability(db_session):
    """Test creating an availability via repository"""
    # First create an employee
    employee_repo = EmployeeRepository(db_session)
    employee = employee_repo.create({
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "role_id": 1,
        "contract_type_id": 1
    })
    
    repo = AvailabilityRepository(db_session)
    availability_data = {
        "employee_id": employee.id,
        "start_time": time(9, 0),
        "end_time": time(17, 0),
        "day_of_week": 0,
        "is_recurring": True,
        "is_active": True
    }
    availability = repo.create(availability_data)
    
    assert availability.id is not None
    assert availability.employee_id == employee.id
    assert availability.start_time == time(9, 0)
    assert availability.end_time == time(17, 0)
    assert availability.day_of_week == 0
    assert availability.is_recurring is True


def test_get_by_employee(db_session):
    """Test retrieving availabilities for an employee"""
    # Create employee
    employee_repo = EmployeeRepository(db_session)
    employee = employee_repo.create({
        "first_name": "Test",
        "last_name": "User2",
        "email": "test2@example.com",
        "role_id": 1,
        "contract_type_id": 1
    })
    
    repo = AvailabilityRepository(db_session)
    
    # Create multiple availabilities
    repo.create({
        "employee_id": employee.id,
        "start_time": time(9, 0),
        "end_time": time(17, 0),
        "day_of_week": 0,
        "is_recurring": True,
        "is_active": True
    })
    repo.create({
        "employee_id": employee.id,
        "start_time": time(9, 0),
        "end_time": time(17, 0),
        "day_of_week": 1,
        "is_recurring": True,
        "is_active": True
    })
    
    availabilities = repo.get_by_employee(employee.id)
    assert len(availabilities) >= 2


def test_get_by_employee_active_only(db_session):
    """Test filtering by active status"""
    # Create employee
    employee_repo = EmployeeRepository(db_session)
    employee = employee_repo.create({
        "first_name": "Test",
        "last_name": "User3",
        "email": "test3@example.com",
        "role_id": 1,
        "contract_type_id": 1
    })
    
    repo = AvailabilityRepository(db_session)
    
    # Create active availability
    repo.create({
        "employee_id": employee.id,
        "start_time": time(9, 0),
        "end_time": time(17, 0),
        "day_of_week": 0,
        "is_recurring": True,
        "is_active": True
    })
    
    # Create inactive availability
    repo.create({
        "employee_id": employee.id,
        "start_time": time(9, 0),
        "end_time": time(17, 0),
        "day_of_week": 1,
        "is_recurring": True,
        "is_active": False
    })
    
    active_availabilities = repo.get_by_employee(employee.id, active_only=True)
    all_availabilities = repo.get_by_employee(employee.id, active_only=False)
    
    assert len(active_availabilities) == 1
    assert len(all_availabilities) == 2


def test_get_by_day(db_session):
    """Test retrieving availabilities for a specific day"""
    # Create employee
    employee_repo = EmployeeRepository(db_session)
    employee = employee_repo.create({
        "first_name": "Test",
        "last_name": "User4",
        "email": "test4@example.com",
        "role_id": 1,
        "contract_type_id": 1
    })
    
    repo = AvailabilityRepository(db_session)
    
    # Create Monday availability
    repo.create({
        "employee_id": employee.id,
        "start_time": time(9, 0),
        "end_time": time(17, 0),
        "day_of_week": 0,
        "is_recurring": True,
        "is_active": True
    })
    
    # Create Tuesday availability
    repo.create({
        "employee_id": employee.id,
        "start_time": time(9, 0),
        "end_time": time(17, 0),
        "day_of_week": 1,
        "is_recurring": True,
        "is_active": True
    })
    
    monday_availabilities = repo.get_by_day(employee.id, 0)
    assert len(monday_availabilities) >= 1
    assert all(av.day_of_week == 0 for av in monday_availabilities)


def test_get_by_specific_date(db_session):
    """Test retrieving availabilities for a specific date"""
    # Create employee
    employee_repo = EmployeeRepository(db_session)
    employee = employee_repo.create({
        "first_name": "Test",
        "last_name": "User5",
        "email": "test5@example.com",
        "role_id": 1,
        "contract_type_id": 1
    })
    
    repo = AvailabilityRepository(db_session)
    specific_date = date(2026, 6, 15)
    
    # Create specific date availability
    repo.create({
        "employee_id": employee.id,
        "start_time": time(10, 0),
        "end_time": time(14, 0),
        "specific_date": specific_date,
        "is_recurring": False,
        "is_active": True
    })
    
    availabilities = repo.get_by_specific_date(employee.id, specific_date)
    assert len(availabilities) >= 1
    assert availabilities[0].specific_date == specific_date
    assert availabilities[0].is_recurring is False


def test_check_overlap_recurring(db_session):
    """Test overlap detection for recurring availabilities"""
    # Create employee
    employee_repo = EmployeeRepository(db_session)
    employee = employee_repo.create({
        "first_name": "Test",
        "last_name": "User6",
        "email": "test6@example.com",
        "role_id": 1,
        "contract_type_id": 1
    })
    
    repo = AvailabilityRepository(db_session)
    
    # Create Monday 9-17 availability
    repo.create({
        "employee_id": employee.id,
        "start_time": time(9, 0),
        "end_time": time(17, 0),
        "day_of_week": 0,
        "is_recurring": True,
        "is_active": True
    })
    
    # Check for overlap with 10-12 (should overlap)
    has_overlap = repo.check_overlap(
        employee_id=employee.id,
        start_time=time(10, 0),
        end_time=time(12, 0),
        day_of_week=0
    )
    assert has_overlap is True
    
    # Check for overlap with Tuesday (should not overlap)
    has_overlap = repo.check_overlap(
        employee_id=employee.id,
        start_time=time(10, 0),
        end_time=time(12, 0),
        day_of_week=1
    )
    assert has_overlap is False


def test_check_overlap_specific_date(db_session):
    """Test overlap detection for specific date availabilities"""
    # Create employee
    employee_repo = EmployeeRepository(db_session)
    employee = employee_repo.create({
        "first_name": "Test",
        "last_name": "User7",
        "email": "test7@example.com",
        "role_id": 1,
        "contract_type_id": 1
    })
    
    repo = AvailabilityRepository(db_session)
    specific_date = date(2026, 6, 20)
    
    # Create specific date availability
    repo.create({
        "employee_id": employee.id,
        "start_time": time(10, 0),
        "end_time": time(14, 0),
        "specific_date": specific_date,
        "is_recurring": False,
        "is_active": True
    })
    
    # Check for overlap with same date (should overlap)
    has_overlap = repo.check_overlap(
        employee_id=employee.id,
        start_time=time(11, 0),
        end_time=time(13, 0),
        specific_date=specific_date
    )
    assert has_overlap is True
    
    # Check for overlap with different date (should not overlap)
    has_overlap = repo.check_overlap(
        employee_id=employee.id,
        start_time=time(11, 0),
        end_time=time(13, 0),
        specific_date=date(2026, 6, 21)
    )
    assert has_overlap is False


def test_check_overlap_exclude_id(db_session):
    """Test that exclude_id parameter works in overlap check"""
    # Create employee
    employee_repo = EmployeeRepository(db_session)
    employee = employee_repo.create({
        "first_name": "Test",
        "last_name": "User8",
        "email": "test8@example.com",
        "role_id": 1,
        "contract_type_id": 1
    })
    
    repo = AvailabilityRepository(db_session)
    
    # Create availability
    availability = repo.create({
        "employee_id": employee.id,
        "start_time": time(9, 0),
        "end_time": time(17, 0),
        "day_of_week": 0,
        "is_recurring": True,
        "is_active": True
    })
    
    # Check overlap excluding this availability (should not overlap with itself)
    has_overlap = repo.check_overlap(
        employee_id=employee.id,
        start_time=time(9, 0),
        end_time=time(17, 0),
        day_of_week=0,
        exclude_id=availability.id
    )
    assert has_overlap is False


def test_get_recurring_availabilities(db_session):
    """Test getting only recurring availabilities"""
    # Create employee
    employee_repo = EmployeeRepository(db_session)
    employee = employee_repo.create({
        "first_name": "Test",
        "last_name": "User9",
        "email": "test9@example.com",
        "role_id": 1,
        "contract_type_id": 1
    })
    
    repo = AvailabilityRepository(db_session)
    
    # Create recurring availability
    repo.create({
        "employee_id": employee.id,
        "start_time": time(9, 0),
        "end_time": time(17, 0),
        "day_of_week": 0,
        "is_recurring": True,
        "is_active": True
    })
    
    # Create specific date availability
    repo.create({
        "employee_id": employee.id,
        "start_time": time(10, 0),
        "end_time": time(14, 0),
        "specific_date": date(2026, 6, 25),
        "is_recurring": False,
        "is_active": True
    })
    
    recurring = repo.get_recurring_availabilities(employee.id)
    assert all(av.is_recurring is True for av in recurring)


def test_get_specific_date_availabilities(db_session):
    """Test getting only specific date availabilities"""
    # Create employee
    employee_repo = EmployeeRepository(db_session)
    employee = employee_repo.create({
        "first_name": "Test",
        "last_name": "User10",
        "email": "test10@example.com",
        "role_id": 1,
        "contract_type_id": 1
    })
    
    repo = AvailabilityRepository(db_session)
    
    # Create recurring availability
    repo.create({
        "employee_id": employee.id,
        "start_time": time(9, 0),
        "end_time": time(17, 0),
        "day_of_week": 0,
        "is_recurring": True,
        "is_active": True
    })
    
    # Create specific date availability
    repo.create({
        "employee_id": employee.id,
        "start_time": time(10, 0),
        "end_time": time(14, 0),
        "specific_date": date(2026, 6, 25),
        "is_recurring": False,
        "is_active": True
    })
    
    specific_dates = repo.get_specific_date_availabilities(employee.id)
    assert all(av.is_recurring is False for av in specific_dates)

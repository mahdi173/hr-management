import pytest
from datetime import date
from app.repositories.absence_repository import AbsenceRepository, AbsenceTypeRepository
from app.models.absence import AbsenceStatus

def test_create_absence_type(db_session):
    repo = AbsenceTypeRepository(db_session)
    data = {"name": "Test Leave", "requires_approval": True, "is_paid": True}
    absence_type = repo.create(data)
    assert absence_type.id is not None
    assert absence_type.name == "Test Leave"

def test_create_absence_request(db_session):
    # Need an employee and absence type first
    from app.models.employee import Employee
    from app.models.absence import AbsenceType
    
    emp = Employee(first_name="Test", last_name="User", email="test@example.com")
    db_session.add(emp)
    abt = AbsenceType(name="Vacation", requires_approval=True, is_paid=True)
    db_session.add(abt)
    db_session.commit()
    
    repo = AbsenceRepository(db_session)
    data = {
        "employee_id": emp.id,
        "absence_type_id": abt.id,
        "start_date": date(2026, 6, 1),
        "end_date": date(2026, 6, 5),
        "reason": "Holiday",
        "status": AbsenceStatus.PENDING
    }
    absence = repo.create(data)
    assert absence.id is not None
    assert absence.status == AbsenceStatus.PENDING

def test_get_by_employee(db_session):
    from app.models.employee import Employee
    from app.models.absence import AbsenceType, Absence
    
    emp = Employee(first_name="Test", last_name="User", email="test2@example.com")
    db_session.add(emp)
    abt = AbsenceType(name="Sick", requires_approval=True, is_paid=True)
    db_session.add(abt)
    db_session.commit()
    
    repo = AbsenceRepository(db_session)
    repo.create({
        "employee_id": emp.id,
        "absence_type_id": abt.id,
        "start_date": date(2026, 6, 1),
        "end_date": date(2026, 6, 2)
    })
    
    absences = repo.get_by_employee(emp.id)
    assert len(absences) == 1
    assert absences[0].employee_id == emp.id

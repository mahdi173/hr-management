import pytest
from fastapi import status
from datetime import date

def test_create_absence_success(client, db_session):
    # Setup
    from app.models.employee import Employee
    from app.models.absence import AbsenceType
    emp = Employee(first_name="John", last_name="Doe", email="john@example.com")
    db_session.add(emp)
    abt = AbsenceType(name="Vacation", requires_approval=True, is_paid=True)
    db_session.add(abt)
    db_session.commit()
    
    response = client.post(
        "/absences/",
        json={
            "employee_id": emp.id,
            "absence_type_id": abt.id,
            "start_date": "2026-06-01",
            "end_date": "2026-06-05",
            "reason": "Trip"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == "pending"

def test_approve_absence(client, db_session):
    # Setup
    from app.models.employee import Employee
    from app.models.absence import AbsenceType, Absence, AbsenceStatus
    emp = Employee(first_name="John", last_name="Doe", email="john2@example.com")
    mgr = Employee(first_name="Boss", last_name="Man", email="boss@example.com")
    db_session.add_all([emp, mgr])
    abt = AbsenceType(name="Sick", requires_approval=True, is_paid=True)
    db_session.add(abt)
    db_session.commit()
    
    abs_req = Absence(
        employee_id=emp.id,
        absence_type_id=abt.id,
        start_date=date(2026, 6, 1),
        end_date=date(2026, 6, 2),
        status=AbsenceStatus.PENDING
    )
    db_session.add(abs_req)
    db_session.commit()
    
    response = client.put(f"/absences/{abs_req.id}/approve?manager_id={mgr.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "approved"
    assert response.json()["approved_by_id"] == mgr.id

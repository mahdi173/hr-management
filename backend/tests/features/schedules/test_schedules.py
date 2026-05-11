import pytest
from fastapi import status
from datetime import date

def test_create_schedule_success(client, db_session):
    from app.models.employee import Employee
    emp = Employee(first_name="Admin", last_name="User", email="admin@example.com")
    db_session.add(emp)
    db_session.commit()
    
    response = client.post(
        "/schedules/",
        json={
            "name": "July Schedule",
            "start_date": "2026-07-01",
            "end_date": "2026-07-31",
            "created_by_id": emp.id
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "July Schedule"

def test_list_schedules(client, db_session):
    from app.models.employee import Employee
    from app.models.schedule import Schedule
    emp = Employee(first_name="Admin", last_name="User", email="admin2@example.com")
    db_session.add(emp)
    db_session.commit()
    
    s1 = Schedule(name="S1", start_date=date(2026, 8, 1), end_date=date(2026, 8, 7), created_by_id=emp.id)
    db_session.add(s1)
    db_session.commit()
    
    response = client.get("/schedules/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 1

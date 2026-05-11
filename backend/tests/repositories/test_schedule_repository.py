import pytest
from datetime import date
from app.repositories.schedule_repository import ScheduleRepository
from app.models.schedule import ScheduleStatus

def test_create_schedule(db_session):
    from app.models.employee import Employee
    emp = Employee(first_name="Manager", last_name="User", email="mgr@example.com")
    db_session.add(emp)
    db_session.commit()
    
    repo = ScheduleRepository(db_session)
    data = {
        "name": "June Week 1",
        "start_date": date(2026, 6, 1),
        "end_date": date(2026, 6, 7),
        "created_by_id": emp.id,
        "status": ScheduleStatus.DRAFT
    }
    schedule = repo.create(data)
    assert schedule.id is not None
    assert schedule.name == "June Week 1"
    assert schedule.status == ScheduleStatus.DRAFT

def test_get_by_date_range(db_session):
    from app.models.employee import Employee
    emp = Employee(first_name="Manager", last_name="User", email="mgr2@example.com")
    db_session.add(emp)
    db_session.commit()
    
    repo = ScheduleRepository(db_session)
    repo.create({
        "name": "June",
        "start_date": date(2026, 6, 1),
        "end_date": date(2026, 6, 30),
        "created_by_id": emp.id
    })
    
    # Overlapping range
    schedules = repo.get_by_date_range(date(2026, 6, 15), date(2026, 7, 5))
    assert len(schedules) == 1
    
    # Outside range
    schedules = repo.get_by_date_range(date(2026, 7, 1), date(2026, 7, 10))
    assert len(schedules) == 0

"""Get Absences Controller - HTTP endpoints for listing absence requests"""

from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared.absence_dto import AbsenceResponse, AbsenceStatus
from .get_absences_usecase import GetAbsencesUseCase

router = APIRouter()


@router.get("/", response_model=List[AbsenceResponse])
def list_absences(
    employee_id: Optional[int] = None,
    status: Optional[AbsenceStatus] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List absence requests with optional filters"""
    use_case = GetAbsencesUseCase(db)
    return use_case.execute_list(employee_id, status, skip, limit)


@router.get("/{absence_id}", response_model=AbsenceResponse)
def get_absence(absence_id: int, db: Session = Depends(get_db)):
    """Get a single absence request by ID"""
    use_case = GetAbsencesUseCase(db)
    return use_case.execute_one(absence_id)

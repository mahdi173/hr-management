"""Create Absence Controller - HTTP endpoints for requesting absences"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared.absence_dto import AbsenceCreate, AbsenceResponse
from .create_absence_usecase import CreateAbsenceUseCase

router = APIRouter()


@router.post("/", response_model=AbsenceResponse, status_code=status.HTTP_201_CREATED)
def create_absence(absence_data: AbsenceCreate, db: Session = Depends(get_db)):
    """
    Submit a new absence request
    
    Args:
        absence_data: Absence creation data
        db: Database session
        
    Returns:
        Created absence instance
    """
    use_case = CreateAbsenceUseCase(db)
    return use_case.execute(absence_data)

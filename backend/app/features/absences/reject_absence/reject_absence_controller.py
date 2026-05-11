"""Reject Absence Controller - HTTP endpoints for rejecting absence requests"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared.absence_dto import AbsenceResponse
from .reject_absence_usecase import RejectAbsenceUseCase

router = APIRouter()


@router.put("/{absence_id}/reject", response_model=AbsenceResponse)
def reject_absence(absence_id: int, db: Session = Depends(get_db)):
    """
    Reject a pending absence request
    
    Args:
        absence_id: ID of the absence request
        db: Database session
        
    Returns:
        Updated absence instance
    """
    use_case = RejectAbsenceUseCase(db)
    return use_case.execute(absence_id)

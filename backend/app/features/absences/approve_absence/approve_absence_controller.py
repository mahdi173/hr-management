"""Approve Absence Controller - HTTP endpoints for approving absence requests"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared.absence_dto import AbsenceResponse
from .approve_absence_usecase import ApproveAbsenceUseCase

router = APIRouter()


@router.put("/{absence_id}/approve", response_model=AbsenceResponse)
def approve_absence(absence_id: int, manager_id: int, db: Session = Depends(get_db)):
    """
    Approve a pending absence request
    
    Args:
        absence_id: ID of the absence request
        manager_id: ID of the manager approving (passed as query param for now)
        db: Database session
        
    Returns:
        Updated absence instance
    """
    use_case = ApproveAbsenceUseCase(db)
    return use_case.execute(absence_id, manager_id)

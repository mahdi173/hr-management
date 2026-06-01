"""Reject Absence Controller - HTTP endpoints for rejecting absence requests"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....core.dependencies import require_manager
from ....database import get_db
from ....models.user import User
from ..shared.absence_dto import AbsenceResponse
from .reject_absence_usecase import RejectAbsenceUseCase

router = APIRouter()


@router.put("/{absence_id}/reject", response_model=AbsenceResponse)
def reject_absence(
    absence_id: int,
    _current_user: User = Depends(require_manager),
    db: Session = Depends(get_db),
):
    use_case = RejectAbsenceUseCase(db)
    return use_case.execute(absence_id)

"""Approve Absence Controller - HTTP endpoints for approving absence requests"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....core.dependencies import require_manager
from ....database import get_db
from ....models.user import User
from ..shared.absence_dto import AbsenceResponse
from .approve_absence_usecase import ApproveAbsenceUseCase

router = APIRouter()


@router.put("/{absence_id}/approve", response_model=AbsenceResponse)
def approve_absence(
    absence_id: int,
    current_user: User = Depends(require_manager),
    db: Session = Depends(get_db),
):
    if not current_user.employee_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Manager must be linked to an employee profile",
        )
    use_case = ApproveAbsenceUseCase(db)
    return use_case.execute(absence_id, current_user.employee_id)

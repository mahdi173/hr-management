"""Get Absences Controller - HTTP endpoints for listing absence requests"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....core.authorization import is_admin_or_manager
from ....core.dependencies import get_current_user, require_manager
from ....database import get_db
from ....models.user import User
from ..shared.absence_dto import AbsenceResponse, AbsenceStatus
from .get_absences_usecase import GetAbsencesUseCase

router = APIRouter()


@router.get("/", response_model=List[AbsenceResponse])
def list_absences(
    employee_id: Optional[int] = None,
    absence_status: Optional[AbsenceStatus] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_manager),
    db: Session = Depends(get_db),
):
    use_case = GetAbsencesUseCase(db)
    return use_case.execute_list(employee_id, absence_status, skip, limit)


@router.get("/{absence_id}", response_model=AbsenceResponse)
def get_absence(
    absence_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    use_case = GetAbsencesUseCase(db)
    absence = use_case.execute_one(absence_id)
    if not is_admin_or_manager(current_user):
        if not current_user.employee_id or absence.employee_id != current_user.employee_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this resource",
            )
    return absence

"""Get My Absences Controller - GET /absences/me"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ....core.dependencies import get_current_user
from ....database import get_db
from ....models.user import User
from ..get_absences.get_absences_usecase import GetAbsencesUseCase
from ..shared.absence_dto import AbsenceResponse, AbsenceStatus

router = APIRouter()


@router.get("/me", response_model=List[AbsenceResponse])
def get_my_absences(
    status_filter: Optional[AbsenceStatus] = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.employee_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not linked to an employee profile",
        )

    use_case = GetAbsencesUseCase(db)
    return use_case.execute_list(
        employee_id=current_user.employee_id,
        status=status_filter,
        skip=skip,
        limit=limit,
    )

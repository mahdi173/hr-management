"""Create Absence Controller - HTTP endpoints for requesting absences"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ....core.authorization import verify_resource_access
from ....core.dependencies import get_current_user
from ....database import get_db
from ....models.user import User
from ..shared.absence_dto import AbsenceCreate, AbsenceResponse
from .create_absence_usecase import CreateAbsenceUseCase

router = APIRouter()


@router.post("/", response_model=AbsenceResponse, status_code=status.HTTP_201_CREATED)
def create_absence(
    absence_data: AbsenceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_resource_access(current_user, absence_data.employee_id)
    use_case = CreateAbsenceUseCase(db)
    return use_case.execute(absence_data)

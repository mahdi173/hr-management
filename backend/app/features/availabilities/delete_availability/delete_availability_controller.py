"""Delete Availability Controller - HTTP endpoint for deleting availabilities"""

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from ....core.authorization import verify_availability_access
from ....core.dependencies import get_current_user
from ....database import get_db
from ....models.user import User
from .delete_availability_usecase import DeleteAvailabilityUseCase

router = APIRouter()


@router.delete(
    "/availabilities/{availability_id}",
    summary="Delete an availability",
)
def delete_availability(
    availability_id: int = Path(..., gt=0, description="The ID of the availability"),
    hard_delete: bool = Query(False, description="Permanently delete if true"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_availability_access(current_user, db, availability_id)
    use_case = DeleteAvailabilityUseCase(db)
    return use_case.execute(availability_id, hard_delete=hard_delete)

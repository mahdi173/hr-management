"""Delete Availability Controller - HTTP endpoint for deleting availabilities"""

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from ....database import get_db
from .delete_availability_usecase import DeleteAvailabilityUseCase

router = APIRouter()


@router.delete(
    "/availabilities/{availability_id}",
    summary="Delete an availability",
    description="Delete an availability. By default performs soft delete (deactivates), use hard_delete=true to permanently remove.",
    responses={
        200: {"description": "Availability deleted successfully"},
        404: {"description": "Availability not found"},
    }
)
def delete_availability(
    availability_id: int = Path(..., gt=0, description="The ID of the availability to delete"),
    hard_delete: bool = Query(False, description="If true, permanently delete; if false, soft delete (default)"),
    db: Session = Depends(get_db)
):
    """
    Delete an availability
    
    - **availability_id**: Unique identifier of the availability to delete
    - **hard_delete**: If true, permanently deletes the record; if false, just deactivates it (default: false)
    """
    use_case = DeleteAvailabilityUseCase(db)
    return use_case.execute(availability_id, hard_delete=hard_delete)

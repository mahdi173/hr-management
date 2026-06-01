"""Delete Shift Controller - HTTP endpoint for deleting shifts"""

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from ....database import get_db
from .delete_shift_usecase import DeleteShiftUseCase

router = APIRouter()


@router.delete(
    "/shifts/{shift_id}",
    summary="Delete a shift",
    description="Delete a shift by ID. Requires manager authorization. By default performs soft delete, use hard_delete=true to permanently remove.",
    responses={
        200: {"description": "Shift deleted successfully"},
        404: {"description": "Shift not found"},
        400: {"description": "Cannot delete shift with active assignments"},
        403: {"description": "Unauthorized - manager ID required"},
    },
    tags=["shifts"]
)
def delete_shift(
    shift_id: int = Path(..., gt=0, description="The ID of the shift to delete"),
    manager_id: int = Query(..., gt=0, description="ID of the manager authorizing the deletion"),
    hard_delete: bool = Query(False, description="If true, permanently delete; if false, soft delete (default)"),
    force: bool = Query(False, description="If true, delete even if there are active assignments (default: false)"),
    db: Session = Depends(get_db)
):
    """
    Delete a shift
    
    - **shift_id**: Unique identifier of the shift to delete
    - **manager_id**: ID of the manager authorizing this deletion (required for authorization tracking)
    - **hard_delete**: If true, permanently deletes the record; if false, marks as inactive (default: false)
    - **force**: If true, allows deletion even with active assignments (default: false)
    
    Note: By default, shifts with active employee assignments cannot be deleted unless force=true is specified.
    """
    use_case = DeleteShiftUseCase(db)
    return use_case.execute(
        shift_id=shift_id,
        manager_id=manager_id,
        hard_delete=hard_delete,
        force=force
    )

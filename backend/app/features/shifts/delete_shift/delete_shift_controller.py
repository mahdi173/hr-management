"""Delete Shift Controller - HTTP endpoints for deleting shifts"""

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from ....database import get_db
from .delete_shift_usecase import DeleteShiftUseCase

router = APIRouter()


@router.delete(
    "/shifts/{shift_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a shift",
    tags=["shifts"]
)
def delete_shift(shift_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing shift
    
    - **shift_id**: ID of the shift to delete
    """
    use_case = DeleteShiftUseCase(db)
    use_case.execute(shift_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

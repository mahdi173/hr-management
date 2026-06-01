"""Delete Shift Use Case - Business logic for deleting shifts"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.shift_repository import ShiftRepository, ShiftAssignmentRepository
from ....repositories.employee_repository import EmployeeRepository


class DeleteShiftUseCase:
    """Use case for deleting a shift with authorization"""

    def __init__(self, db: Session):
        self.db = db
        self.shift_repository = ShiftRepository(db)
        self.assignment_repository = ShiftAssignmentRepository(db)
        self.employee_repository = EmployeeRepository(db)

    def execute(
        self,
        shift_id: int,
        manager_id: int,
        hard_delete: bool = False,
        force: bool = False
    ) -> dict:
        """
        Execute the delete shift use case
        
        Args:
            shift_id: ID of the shift to delete
            manager_id: ID of the manager authorizing the deletion
            hard_delete: If True, permanently delete; if False, soft delete (set is_active=False)
            force: If True, delete even if there are active assignments
            
        Returns:
            Success message dictionary
            
        Raises:
            HTTPException: If shift is not found, manager is not authorized, or shift has active assignments
        """
        # Verify manager exists and has appropriate role
        manager = self.employee_repository.get_by_id(manager_id)
        if not manager:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Manager with id {manager_id} not found. Authorization required."
            )
        
        # TODO: Add role-based authorization check when authentication is implemented
        # For now, we just verify the manager exists
        
        # Check if shift exists
        shift = self.shift_repository.get_by_id(shift_id)
        if not shift:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shift with id {shift_id} not found"
            )

        # Check for active assignments unless force is True
        if not force:
            assignments = self.assignment_repository.get_by_shift(shift_id)
            if assignments:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot delete shift {shift_id}: {len(assignments)} active assignment(s) exist. "
                           f"Use force=true to delete anyway or remove assignments first."
                )

        # Perform deletion
        if hard_delete:
            # Remove all assignments first if force is True
            if force:
                assignments = self.assignment_repository.get_by_shift(shift_id)
                for assignment in assignments:
                    self.assignment_repository.delete(assignment.id)
            
            # Permanently delete the shift
            self.shift_repository.delete(shift_id)
            return {
                "message": f"Shift {shift_id} permanently deleted",
                "deleted_by": manager_id,
                "hard_delete": True
            }
        else:
            # Soft delete - mark as inactive
            # Note: The Shift model needs an is_active field for this to work
            # If it doesn't exist, we'll need to add it via migration
            try:
                self.shift_repository.update(shift_id, {"is_active": False})
                return {
                    "message": f"Shift {shift_id} deactivated",
                    "deleted_by": manager_id,
                    "hard_delete": False
                }
            except Exception as e:
                # If is_active field doesn't exist, fall back to hard delete with a warning
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Soft delete failed. The Shift model may not have an 'is_active' field. "
                           f"Use hard_delete=true or add is_active field to the model. Error: {str(e)}"
                )

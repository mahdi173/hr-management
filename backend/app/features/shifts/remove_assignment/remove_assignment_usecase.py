"""Remove Employee Assignment Use Case - Business logic for removing shift assignments"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ....repositories.shift_repository import ShiftRepository, ShiftAssignmentRepository


class RemoveAssignmentUseCase:
    """Use case for removing an employee from a shift"""
    
    def __init__(self, db: Session):
        self.db = db
        self.shift_repo = ShiftRepository(db)
        self.assignment_repo = ShiftAssignmentRepository(db)
    
    def execute(self, shift_id: int, employee_id: int) -> dict:
        """
        Remove an employee assignment from a shift
        
        Business rules:
        - Shift must exist
        - Assignment must exist
        - Cannot remove if it would violate min_employees constraint
        """
        # Validate shift exists
        shift = self.shift_repo.get_by_id(shift_id)
        if not shift:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shift with id {shift_id} not found"
            )
        
        # Find the assignment
        assignment = self.assignment_repo.get_by_employee_and_shift(employee_id, shift_id)
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No assignment found for employee {employee_id} on shift {shift_id}"
            )
        
        # Check if removing would violate min_employees
        current_count = self.assignment_repo.count_assignments_for_shift(shift_id)
        if current_count <= shift.min_employees:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot remove assignment. Shift requires minimum {shift.min_employees} employee(s)"
            )
        
        # Delete the assignment
        self.assignment_repo.delete(assignment.id)
        
        return {
            "message": f"Employee {employee_id} removed from shift {shift_id}",
            "shift_id": shift_id,
            "employee_id": employee_id
        }

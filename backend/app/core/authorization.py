"""
Authorization utilities - resource ownership validation.
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.user import User
from ..repositories.availability_repository import AvailabilityRepository


def is_admin_or_manager(user: User) -> bool:
    """Return True if the user has Admin, Manager, or Team Lead role."""
    if not user.employee or not user.employee.role:
        return False
    return user.employee.role.name in ["Admin", "Manager", "Team Lead"]


def verify_resource_access(current_user: User, resource_employee_id: int) -> bool:
    """
    Verify access to a resource owned by resource_employee_id.
    Admins/managers may access any resource; others only their own.
    """
    if is_admin_or_manager(current_user):
        return True

    if current_user.employee_id and current_user.employee_id == resource_employee_id:
        return True

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have access to this resource",
    )


def verify_availability_access(
    current_user: User, db: Session, availability_id: int
):
    """Load an availability and verify the current user may access it."""
    availability = AvailabilityRepository(db).get_by_id(availability_id)
    if not availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Availability with id {availability_id} not found",
        )
    verify_resource_access(current_user, availability.employee_id)
    return availability

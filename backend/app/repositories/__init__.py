"""Repository layer for database operations"""

from .base import BaseRepository
from .employee_repository import EmployeeRepository

__all__ = ["BaseRepository", "EmployeeRepository"]

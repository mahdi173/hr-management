"""Delete Employee Feature"""

from .delete_employee_usecase import DeleteEmployeeUseCase
from .delete_employee_controller import router

__all__ = ["DeleteEmployeeUseCase", "router"]

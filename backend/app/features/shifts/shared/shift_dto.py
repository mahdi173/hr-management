"""Shift and ShiftAssignment Data Transfer Objects - Shared across shift features"""

from pydantic import BaseModel, Field, model_validator
from datetime import date as date_type, datetime as datetime_type, time as time_type
from typing import Optional, List
from ....models.shift import ShiftAssignmentStatus, AssignmentType


# ==================== Shift DTOs ====================

class ShiftBase(BaseModel):
    """Base schema for Shift with shared fields"""
    schedule_id: int = Field(..., description="ID of the schedule this shift belongs to")
    required_role_id: Optional[int] = Field(None, description="ID of the required role for this shift")
    date: date_type = Field(..., description="Date of the shift")
    start_time: time_type = Field(..., description="Start time of the shift")
    end_time: time_type = Field(..., description="End time of the shift")
    min_employees: int = Field(1, ge=1, description="Minimum number of employees required")
    max_employees: int = Field(1, ge=1, description="Maximum number of employees allowed")
    notes: Optional[str] = None

    @model_validator(mode='after')
    def validate_time_order(self):
        """Validate that end_time is after start_time"""
        if self.start_time >= self.end_time:
            raise ValueError('end_time must be after start_time')
        return self

    @model_validator(mode='after')
    def validate_employee_limits(self):
        """Validate that max_employees >= min_employees"""
        if self.max_employees < self.min_employees:
            raise ValueError('max_employees must be greater than or equal to min_employees')
        return self


class ShiftCreate(ShiftBase):
    """Schema for creating a new shift"""
    pass


class ShiftUpdate(BaseModel):
    """Schema for updating an existing shift"""
    required_role_id: Optional[int] = None
    date: Optional[date_type] = None
    start_time: Optional[time_type] = None
    end_time: Optional[time_type] = None
    min_employees: Optional[int] = Field(None, ge=1)
    max_employees: Optional[int] = Field(None, ge=1)
    notes: Optional[str] = None


class ShiftAssignmentSummary(BaseModel):
    """Summary of shift assignment for nested response"""
    id: int
    employee_id: int
    status: ShiftAssignmentStatus
    assignment_type: AssignmentType
    is_overtime: bool
    
    class Config:
        from_attributes = True


class ShiftResponse(ShiftBase):
    """Schema for shift response with database fields"""
    id: int
    created_at: datetime_type
    updated_at: Optional[datetime_type] = None
    assignments: List[ShiftAssignmentSummary] = []

    class Config:
        from_attributes = True


# ==================== ShiftAssignment DTOs ====================

class ShiftAssignmentBase(BaseModel):
    """Base schema for ShiftAssignment"""
    shift_id: int = Field(..., description="ID of the shift")
    employee_id: int = Field(..., description="ID of the employee")
    assignment_type: AssignmentType = Field(AssignmentType.REGULAR, description="Type of assignment")
    is_overtime: bool = Field(False, description="Whether this is overtime work")


class ShiftAssignmentCreate(ShiftAssignmentBase):
    """Schema for creating a shift assignment"""
    pass


class ShiftAssignmentUpdate(BaseModel):
    """Schema for updating a shift assignment"""
    status: Optional[ShiftAssignmentStatus] = None
    assignment_type: Optional[AssignmentType] = None
    is_overtime: Optional[bool] = None


class ShiftAssignmentResponse(ShiftAssignmentBase):
    """Schema for shift assignment response"""
    id: int
    status: ShiftAssignmentStatus
    created_at: datetime_type

    class Config:
        from_attributes = True


# ==================== Working Hours DTOs (US 1.8) ====================

class HoursSummary(BaseModel):
    """Summary of working hours for an employee"""
    employee_id: int
    period_start: date_type
    period_end: date_type
    total_hours: float = Field(..., description="Total hours worked")
    regular_hours: float = Field(..., description="Regular hours worked")
    overtime_hours: float = Field(..., description="Overtime hours worked")
    assignment_count: int = Field(..., description="Number of shift assignments")


class ShiftWithHours(BaseModel):
    """Shift information with calculated hours"""
    shift_id: int
    date: date_type
    start_time: time_type
    end_time: time_type
    duration_hours: float
    is_overtime: bool
    assignment_type: AssignmentType

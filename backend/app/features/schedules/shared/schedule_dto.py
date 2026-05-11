"""Schedule Data Transfer Objects - Shared across schedule features"""

from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional, List
from ....models.schedule import ScheduleStatus


class ScheduleBase(BaseModel):
    """Base schema for Schedule with shared fields"""
    name: str = Field(..., description="Name of the schedule")
    description: Optional[str] = None
    start_date: date = Field(..., description="Start date of the schedule period")
    end_date: date = Field(..., description="End date of the schedule period")
    created_by_id: int = Field(..., description="ID of the employee who created the schedule")

    @field_validator('end_date')
    @classmethod
    def validate_dates(cls, v: date, info) -> date:
        """Validate that end_date is after or equal to start_date"""
        if 'start_date' in info.data and v < info.data['start_date']:
            raise ValueError('end_date must be after or equal to start_date')
        return v


class ScheduleCreate(ScheduleBase):
    """Schema for creating a new schedule"""
    pass


class ScheduleUpdate(BaseModel):
    """Schema for updating an existing schedule"""
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[ScheduleStatus] = None


class ScheduleResponse(ScheduleBase):
    """Schema for schedule response with database fields"""
    id: int
    status: ScheduleStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

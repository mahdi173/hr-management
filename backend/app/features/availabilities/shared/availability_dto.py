"""Availability Data Transfer Objects - Shared across availability features"""

from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import time, date
from typing import Optional


class AvailabilityBase(BaseModel):
    """Base schema for Availability with shared fields"""
    employee_id: int = Field(
        ...,
        gt=0,
        description="ID of the employee",
        examples=[1]
    )
    start_time: time = Field(
        ...,
        description="Start time of availability",
        examples=["09:00:00"]
    )
    end_time: time = Field(
        ...,
        description="End time of availability",
        examples=["17:00:00"]
    )
    day_of_week: Optional[int] = Field(
        None,
        ge=0,
        le=6,
        description="Day of week (0=Monday, 6=Sunday) for recurring availability, null for specific dates",
        examples=[0]
    )
    is_recurring: bool = Field(
        default=True,
        description="Whether this is a recurring weekly availability"
    )
    specific_date: Optional[date] = Field(
        None,
        description="Specific date for non-recurring availability",
        examples=["2026-05-15"]
    )
    is_active: bool = Field(
        default=True,
        description="Whether the availability is currently active"
    )

    @model_validator(mode='after')
    def validate_time_order(self):
        """Validate that end_time is after start_time"""
        if self.end_time <= self.start_time:
            raise ValueError('end_time must be after start_time')
        return self


class AvailabilityCreate(AvailabilityBase):
    """Schema for creating a new availability"""
    
    @model_validator(mode='after')
    def validate_recurring_fields(self):
        """Validate fields based on is_recurring"""
        if self.is_recurring:
            if self.day_of_week is None:
                raise ValueError('day_of_week is required when is_recurring is True')
            if self.specific_date is not None:
                raise ValueError('specific_date should be null when is_recurring is True')
        else:
            if self.specific_date is None:
                raise ValueError('specific_date is required when is_recurring is False')
            if self.day_of_week is not None:
                raise ValueError('day_of_week should be null when is_recurring is False')
        return self


class AvailabilityUpdate(BaseModel):
    """Schema for updating an existing availability (all fields optional)"""
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_active: Optional[bool] = None

    @model_validator(mode='after')
    def validate_time_order(self):
        """Validate that end_time is after start_time if both are provided"""
        if self.end_time and self.start_time:
            if self.end_time <= self.start_time:
                raise ValueError('end_time must be after start_time')
        return self


class AvailabilityResponse(AvailabilityBase):
    """Schema for availability response with database fields"""
    id: int = Field(..., description="Unique identifier for the availability")

    class Config:
        from_attributes = True

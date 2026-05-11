"""Absence Data Transfer Objects - Shared across absence features"""

from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional, List
from ...absences.shared.absence_dto import AbsenceStatus # I will define it here instead of importing if it causes circular, but let's check model

# Import status from model to keep it consistent
from ....models.absence import AbsenceStatus


class AbsenceTypeResponse(BaseModel):
    """Schema for AbsenceType response"""
    id: int
    name: str
    description: Optional[str] = None
    requires_approval: bool
    is_paid: bool

    class Config:
        from_attributes = True


class AbsenceBase(BaseModel):
    """Base schema for Absence with shared fields"""
    employee_id: int = Field(..., description="ID of the employee")
    absence_type_id: int = Field(..., description="ID of the absence type")
    start_date: date = Field(..., description="Start date of the absence")
    end_date: date = Field(..., description="End date of the absence")
    reason: Optional[str] = Field(None, description="Reason for the absence request")

    @field_validator('end_date')
    @classmethod
    def validate_dates(cls, v: date, info) -> date:
        """Validate that end_date is after or equal to start_date"""
        if 'start_date' in info.data and v < info.data['start_date']:
            raise ValueError('end_date must be after or equal to start_date')
        return v


class AbsenceCreate(AbsenceBase):
    """Schema for creating a new absence request"""
    pass


class AbsenceUpdate(BaseModel):
    """Schema for updating an existing absence request (before approval)"""
    absence_type_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = None


class AbsenceResponse(AbsenceBase):
    """Schema for absence response with database fields"""
    id: int
    status: AbsenceStatus
    approved_by_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    absence_type: Optional[AbsenceTypeResponse] = None

    class Config:
        from_attributes = True

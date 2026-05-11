"""Employee Data Transfer Objects - Shared across employee features"""

from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime
from typing import Optional
import re


class EmployeeBase(BaseModel):
    """Base schema for Employee with shared fields"""
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Employee's first name",
        examples=["John"]
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Employee's last name",
        examples=["Doe"]
    )
    email: EmailStr = Field(
        ...,
        description="Employee's unique email address",
        examples=["john.doe@example.com"]
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Employee's phone number",
        examples=["+33 6 12 34 56 78"]
    )
    role_id: Optional[int] = Field(
        None,
        description="ID of the employee's role",
        examples=[1]
    )
    contract_type_id: Optional[int] = Field(
        None,
        description="ID of the employee's contract type",
        examples=[1]
    )
    is_active: bool = Field(
        default=True,
        description="Whether the employee is currently active"
    )

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format"""
        if v is None:
            return v
        # Remove spaces and common separators
        cleaned = re.sub(r'[\s\-\.\(\)]', '', v)
        # Check if it contains only digits and optional + at start
        if not re.match(r'^\+?\d{8,15}$', cleaned):
            raise ValueError('Phone number must contain 8-15 digits and can start with +')
        return v


class EmployeeCreate(EmployeeBase):
    """Schema for creating a new employee"""
    pass


class EmployeeUpdate(BaseModel):
    """Schema for updating an existing employee (all fields optional)"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    role_id: Optional[int] = None
    contract_type_id: Optional[int] = None
    is_active: Optional[bool] = None

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format"""
        if v is None:
            return v
        cleaned = re.sub(r'[\s\-\.\(\)]', '', v)
        if not re.match(r'^\+?\d{8,15}$', cleaned):
            raise ValueError('Phone number must contain 8-15 digits and can start with +')
        return v


class EmployeeResponse(EmployeeBase):
    """Schema for employee response with database fields"""
    id: int = Field(..., description="Unique identifier for the employee")
    created_at: datetime = Field(..., description="Timestamp when the employee was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the employee was last updated")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "+33 6 12 34 56 78",
                "role_id": 1,
                "contract_type_id": 1,
                "is_active": True,
                "created_at": "2026-05-11T10:30:00",
                "updated_at": None
            }
        }

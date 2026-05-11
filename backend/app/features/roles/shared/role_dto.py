"""Role Data Transfer Objects - Shared across role features"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any, Dict


class RoleBase(BaseModel):
    """Base schema for Role with shared fields"""
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the role",
        examples=["Manager"]
    )
    description: Optional[str] = Field(
        None,
        max_length=255,
        description="Description of the role",
        examples=["Full access to system features"]
    )
    permissions: Optional[Dict[str, Any]] = Field(
        None,
        description="Permissions as a JSON object",
        examples=[{"can_edit_users": True, "can_view_reports": True}]
    )
    is_active: bool = Field(
        default=True,
        description="Whether the role is currently active"
    )


class RoleCreate(RoleBase):
    """Schema for creating a new role"""
    pass


class RoleUpdate(BaseModel):
    """Schema for updating an existing role (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    permissions: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class RoleResponse(RoleBase):
    """Schema for role response with database fields"""
    id: int = Field(..., description="Unique identifier for the role")
    created_at: datetime = Field(..., description="Timestamp when the role was created")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Manager",
                "description": "Full access to system features",
                "permissions": {"can_edit_users": True},
                "is_active": True,
                "created_at": "2026-05-11T10:30:00"
            }
        }

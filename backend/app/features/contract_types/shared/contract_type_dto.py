"""ContractType Data Transfer Objects - Shared across contract type features"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ContractTypeBase(BaseModel):
    """Base schema for ContractType with shared fields"""
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the contract type",
        examples=["CDI"]
    )
    description: Optional[str] = Field(
        None,
        max_length=255,
        description="Description of the contract type",
        examples=["Contrat à durée indéterminée"]
    )
    weekly_hours: float = Field(
        ...,
        gt=0,
        le=168,
        description="Default weekly hours for this contract type",
        examples=[35.0]
    )
    max_weekly_hours: Optional[float] = Field(
        None,
        gt=0,
        le=168,
        description="Maximum weekly hours allowed for this contract type",
        examples=[48.0]
    )
    is_active: bool = Field(
        default=True,
        description="Whether the contract type is currently active"
    )


class ContractTypeCreate(ContractTypeBase):
    """Schema for creating a new contract type"""
    pass


class ContractTypeUpdate(BaseModel):
    """Schema for updating an existing contract type (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    weekly_hours: Optional[float] = Field(None, gt=0, le=168)
    max_weekly_hours: Optional[float] = Field(None, gt=0, le=168)
    is_active: Optional[bool] = None


class ContractTypeResponse(ContractTypeBase):
    """Schema for contract type response with database fields"""
    id: int = Field(..., description="Unique identifier for the contract type")

    class Config:
        from_attributes = True

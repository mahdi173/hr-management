from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ItemBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="The title of the item",
        examples=["Buy groceries", "Complete project documentation"]
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Detailed description of the item",
        examples=["Get milk, eggs, and bread from the store"]
    )
    completed: bool = Field(
        default=False,
        description="Whether the item is completed or not"
    )


class ItemCreate(ItemBase):
    """Schema for creating a new item"""
    pass


class Item(ItemBase):
    """Schema for item response with database fields"""
    id: int = Field(..., description="Unique identifier for the item")
    created_at: datetime = Field(..., description="Timestamp when the item was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the item was last updated")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Complete FastAPI tutorial",
                "description": "Learn about API development with FastAPI",
                "completed": False,
                "created_at": "2026-05-11T10:30:00",
                "updated_at": None
            }
        }

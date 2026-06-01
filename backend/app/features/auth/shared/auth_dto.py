"""
Authentication DTOs - Request/Response models for authentication endpoints.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    """Login request with email and password"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response with user information"""
    id: int
    email: str
    role: str
    first_name: str
    last_name: str
    
    class Config:
        from_attributes = True


class TokenPayload(BaseModel):
    """JWT token payload structure"""
    id: int
    email: str
    role: str
    exp: datetime


class TokenData(BaseModel):
    """Optional parsed token data"""
    user_id: Optional[int] = None
    email: Optional[str] = None


class UserInfoResponse(BaseModel):
    """Current user information response"""
    id: int
    email: str
    is_active: bool
    employee_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    
    class Config:
        from_attributes = True

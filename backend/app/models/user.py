"""
User model - for authentication and authorization.
Infrastructure feature (US-0.2).
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Foreign keys
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True, unique=True)
    
    # Relationships
    employee = relationship("Employee", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.email}>"

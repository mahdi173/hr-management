"""Recommendation Data Transfer Objects"""

from pydantic import BaseModel
from typing import List, Optional


class EmployeeRecommendation(BaseModel):
    """Schema for a single employee recommendation"""
    employee_id: int
    employee_name: str
    score: float
    confidence: float
    explanation: str
    conflicts: List[str] = []


class ShiftRecommendations(BaseModel):
    """Schema for recommendations for a specific shift"""
    shift_id: int
    recommendations: List[EmployeeRecommendation]

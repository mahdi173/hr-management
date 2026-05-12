"""Recommendation Controller - endpoints for AI-powered suggestions"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...database import get_db
from ..shifts.shared.recommendation_service import RecommendationService
from ..shifts.shared.recommendation_dto import ShiftRecommendations

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/shift/{shift_id}", response_model=ShiftRecommendations)
def get_recommendations_for_shift(
    shift_id: int,
    db: Session = Depends(get_db)
):
    """
    Get top employee recommendations for a specific shift.
    
    Factors considered:
    - Availability and absence checks
    - Role match
    - Workload balancing
    - Historical shift preferences
    """
    service = RecommendationService(db)
    return service.recommend_for_shift(shift_id)

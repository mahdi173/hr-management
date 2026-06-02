"""Schedule Generation Controller - API endpoints for AI-powered schedule generation"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from ....core.dependencies import require_manager
from ....database import get_db
from ....models.user import User
from ..shared.schedule_generator_service import ScheduleGeneratorService
from ..shared.generation_dto import (
    ScheduleGenerationRequest,
    ScheduleGenerationResponse,
    AssignmentDetail,
    GenerationStats,
    SolvingStats
)

router = APIRouter(prefix="/schedules", tags=["Schedule Generation"])


@router.post("/generate", response_model=ScheduleGenerationResponse)
def generate_schedule(
    request: ScheduleGenerationRequest,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_manager),
):
    """
    Generate an optimized schedule using AI/constraint programming.
    
    **Phase 4 Feature - US-4.1**
    
    This endpoint uses OR-Tools constraint programming to automatically
    generate shift assignments that:
    - Respect all availability and absence constraints
    - Balance workload across employees
    - Maximize schedule completion
    - Comply with weekly hour limits
    
    Returns a complete schedule with quality metrics and warnings.
    """
    try:
        # Parse dates
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d").date()
        
        # Validate date range
        if start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start date must be before or equal to end date"
            )
        
        # Convert shift requirements to dict format
        shift_requirements = [req.model_dump() for req in request.shift_requirements]
        
        # Generate schedule
        service = ScheduleGeneratorService(db)
        result = service.generate_schedule(
            start_date=start_date,
            end_date=end_date,
            shift_requirements=shift_requirements,
            schedule_name=request.schedule_name,
            optimize_for_balance=request.optimize_for_balance
        )
        
        # Convert result to response
        response = ScheduleGenerationResponse(
            success=result.success,
            schedule_id=result.schedule_id,
            assignments=[
                AssignmentDetail(shift_id=a["shift_id"], employee_id=a["employee_id"])
                for a in result.assignments
            ],
            quality_score=result.quality_score,
            warnings=result.warnings,
            errors=result.errors,
            stats=GenerationStats(**result.stats) if result.stats else None,
            solving_stats=SolvingStats(**result.solving_stats) if result.solving_stats else None
        )
        
        if not result.success:
            # Return 200 but with errors in response (partial failure)
            return response
        
        return response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Schedule generation failed: {str(e)}"
        )


@router.get("/generation/status")
def get_generation_status(
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_manager),
):
    """
    Get status and capabilities of the schedule generator.
    
    Useful for UI to check if feature is available and get configuration.
    """
    return {
        "available": True,
        "version": "1.0.0",
        "solver": "OR-Tools CP-SAT",
        "max_solve_time_seconds": 30,
        "features": {
            "constraint_programming": True,
            "workload_balancing": True,
            "availability_checking": True,
            "compliance_validation": True
        },
        "limitations": {
            "max_shifts_per_request": 500,
            "max_employees": 100,
            "timeout_seconds": 30
        }
    }

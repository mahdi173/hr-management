"""DTOs for Schedule Generation API"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import date, time


class ShiftRequirement(BaseModel):
    """Specification for a single shift to be created"""
    date: str = Field(..., description="Shift date in YYYY-MM-DD format")
    start_time: str = Field(..., description="Start time in HH:MM format")
    end_time: str = Field(..., description="End time in HH:MM format")
    required_role_id: int = Field(..., description="ID of required role")
    min_employees: int = Field(1, ge=1, description="Minimum employees needed")
    max_employees: int = Field(1, ge=1, description="Maximum employees allowed")


class ScheduleGenerationRequest(BaseModel):
    """Request to generate a new schedule"""
    start_date: str = Field(..., description="Schedule start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="Schedule end date (YYYY-MM-DD)")
    schedule_name: Optional[str] = Field(None, description="Optional schedule name")
    shift_requirements: List[ShiftRequirement] = Field(..., description="List of shift specifications")
    optimize_for_balance: bool = Field(True, description="Optimize for workload balance")
    
    class Config:
        json_schema_extra = {
            "example": {
                "start_date": "2026-06-10",
                "end_date": "2026-06-16",
                "schedule_name": "Week 24 Schedule",
                "optimize_for_balance": True,
                "shift_requirements": [
                    {
                        "date": "2026-06-10",
                        "start_time": "08:00",
                        "end_time": "12:00",
                        "required_role_id": 1,
                        "min_employees": 1,
                        "max_employees": 2
                    },
                    {
                        "date": "2026-06-10",
                        "start_time": "12:00",
                        "end_time": "18:00",
                        "required_role_id": 1,
                        "min_employees": 2,
                        "max_employees": 3
                    }
                ]
            }
        }


class AssignmentDetail(BaseModel):
    """Details of a single shift assignment"""
    shift_id: int
    employee_id: int


class GenerationStats(BaseModel):
    """Statistics about the generation process"""
    total_shifts: int
    total_assignments: int
    employees_used: int
    fill_rate: float = Field(..., description="Percentage of shifts filled")


class SolvingStats(BaseModel):
    """Statistics from the constraint solver"""
    status: str = Field(..., description="Solver status (OPTIMAL, FEASIBLE, INFEASIBLE)")
    solve_time: float = Field(..., description="Time taken to solve in seconds")
    optimal: bool = Field(..., description="Whether solution is optimal")


class ScheduleGenerationResponse(BaseModel):
    """Response from schedule generation"""
    success: bool
    schedule_id: Optional[int] = None
    assignments: List[AssignmentDetail] = []
    quality_score: float = Field(0.0, ge=0, le=1, description="Overall quality score (0-1)")
    warnings: List[str] = []
    errors: List[str] = []
    stats: Optional[GenerationStats] = None
    solving_stats: Optional[SolvingStats] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "schedule_id": 42,
                "assignments": [
                    {"shift_id": 101, "employee_id": 5},
                    {"shift_id": 101, "employee_id": 8},
                    {"shift_id": 102, "employee_id": 3}
                ],
                "quality_score": 0.87,
                "warnings": ["Shift on 2026-06-11 at 18:00 is under-staffed (1/2)"],
                "errors": [],
                "stats": {
                    "total_shifts": 12,
                    "total_assignments": 20,
                    "employees_used": 8,
                    "fill_rate": 95.2
                },
                "solving_stats": {
                    "status": "OPTIMAL",
                    "solve_time": 2.3,
                    "optimal": True
                }
            }
        }


class TemplateShiftPattern(BaseModel):
    """Shift pattern for a template"""
    day_of_week: int = Field(..., ge=0, le=6, description="Day of week (0=Monday, 6=Sunday)")
    start_time: str = Field(..., description="Start time in HH:MM format")
    end_time: str = Field(..., description="End time in HH:MM format")
    required_role_id: int
    min_employees: int = 1
    max_employees: int = 1


class ScheduleTemplateCreate(BaseModel):
    """Create a new schedule template"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    shift_patterns: List[TemplateShiftPattern] = Field(..., description="Recurring shift patterns")


class ScheduleTemplateResponse(BaseModel):
    """Schedule template details"""
    id: int
    name: str
    description: Optional[str] = None
    shift_patterns: List[Dict[str, Any]]
    
    class Config:
        from_attributes = True

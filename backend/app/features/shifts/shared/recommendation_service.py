"""Recommendation Service - logic for smart employee assignment suggestions"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from datetime import date, time

from ....repositories.employee_repository import EmployeeRepository
from ....repositories.recommendation_repository import RecommendationRepository
from ....repositories.shift_repository import ShiftRepository
from .conflict_service import ConflictDetectionService
from .compliance_service import ComplianceService
from .analytics_service import AnalyticsService
from .recommendation_dto import EmployeeRecommendation, ShiftRecommendations


class RecommendationService:
    """Service to provide AI-powered employee recommendations for shifts"""
    
    def __init__(self, db: Session):
        self.db = db
        self.employee_repo = EmployeeRepository(db)
        self.recommendation_repo = RecommendationRepository(db)
        self.shift_repo = ShiftRepository(db)
        self.conflict_service = ConflictDetectionService(db)
        self.compliance_service = ComplianceService(db)
        self.analytics_service = AnalyticsService(db)
    
    def recommend_for_shift(self, shift_id: int) -> ShiftRecommendations:
        """Get best-fit employees for a specific shift"""
        shift = self.shift_repo.get_by_id(shift_id)
        if not shift:
            return ShiftRecommendations(shift_id=shift_id, recommendations=[])
        
        active_employees = self.employee_repo.get_active_employees()
        recommendations = []
        
        # Get workload analysis for the current week to factor in balance
        start_of_week = shift.date - timedelta(days=shift.date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        workload_summaries = {
            s.employee_id: s for s in self.analytics_service.get_workload_analysis(start_of_week, end_of_week)
        }
        
        for emp in active_employees:
            # 1. Check hard constraints (Conflicts)
            conflicts = self.conflict_service.check_all_conflicts(
                employee_id=emp.id,
                shift_date=shift.date,
                start_time=shift.start_time,
                end_time=shift.end_time
            )
            
            conflict_msgs = [c.message for c in conflicts]
            
            # 2. Check blocking compliance
            compliance = self.compliance_service.validate_assignment(
                employee_id=emp.id,
                shift_date=shift.date,
                start_time=shift.start_time,
                end_time=shift.end_time
            )
            
            if compliance.errors:
                conflict_msgs.extend(compliance.errors)
            
            # If there are hard conflicts/errors, we still might show the employee 
            # but with a very low score and clear conflict list, OR we filter them.
            # Backlog says "Exclude employees with conflicts or absences", so we filter.
            if conflict_msgs:
                continue
                
            # 3. Calculate Scores (0.0 to 1.0)
            
            # Role match score (0.3 weight)
            role_score = 1.0 if emp.role_id == shift.required_role_id else 0.2
            
            # Workload balance score (0.4 weight)
            # Higher score for underutilized, lower for overutilized
            workload_score = 0.5
            if emp.id in workload_summaries:
                utilization = workload_summaries[emp.id].utilization_percentage
                if utilization < 80:
                    workload_score = 0.9
                elif utilization < 100:
                    workload_score = 0.7
                elif utilization < 110:
                    workload_score = 0.3
                else:
                    workload_score = 0.1
            
            # Historical Preference score (0.3 weight)
            # Determine shift type (morning, afternoon, night)
            shift_type = self._get_shift_type(shift.start_time)
            pref_score = self.recommendation_repo.get_preference_score(emp.id, shift_type)
            
            # Weighted Total
            total_score = (role_score * 0.3) + (workload_score * 0.4) + (pref_score * 0.3)
            
            # Confidence Score (simplified for MVP)
            confidence = 0.8 # Constant for now
            
            # Generate Explanation
            explanation = self._generate_explanation(role_score, workload_score, pref_score, emp)
            
            recommendations.append(EmployeeRecommendation(
                employee_id=emp.id,
                employee_name=f"{emp.first_name} {emp.last_name}",
                score=round(total_score, 2),
                confidence=confidence,
                explanation=explanation,
                conflicts=[]
            ))
            
        # Sort by score descending
        recommendations.sort(key=lambda x: x.score, reverse=True)
        
        return ShiftRecommendations(
            shift_id=shift_id,
            recommendations=recommendations[:5] # Top 5 suggestions
        )

    def _get_shift_type(self, start_time: time) -> str:
        """Categorize shift by time of day"""
        if start_time.hour < 12:
            return "morning"
        elif start_time.hour < 18:
            return "afternoon"
        else:
            return "night"

    def _generate_explanation(self, role_score: float, workload_score: float, pref_score: float, emp: Any) -> str:
        """Generate human-readable reason for recommendation"""
        reasons = []
        if role_score > 0.8:
            reasons.append("matches the required role")
        if workload_score > 0.8:
            reasons.append("has low workload this week")
        if pref_score > 0.7:
            reasons.append("typically works this shift type")
            
        if not reasons:
            return f"{emp.first_name} is available and meets all criteria."
            
        return f"{emp.first_name} is recommended because they " + ", ".join(reasons) + "."

from datetime import timedelta # Needed for start_of_week calculation

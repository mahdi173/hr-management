"""
Preference Learning Service - Learn employee scheduling preferences from historical data
Phase 4 - US-4.3: Preference Learning and Personalization
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, time, datetime, timedelta
from collections import defaultdict, Counter
import logging

from ...models.employee import Employee
from ...models.recommendation import AssignmentPreference
from ...models.shift import Shift
from ...repositories.shift_repository import ShiftAssignmentRepository, ShiftRepository
from ...repositories.employee_repository import EmployeeRepository
from ...repositories.recommendation_repository import RecommendationRepository

logger = logging.getLogger(__name__)


class LearnedPreferences(Dict[str, Any]):
    """Container for learned employee preferences"""
    pass


class PreferenceLearningService:
    """Analyze historical assignments to learn employee preferences"""
    
    def __init__(self, db: Session):
        self.db = db
        self.assignment_repo = ShiftAssignmentRepository(db)
        self.shift_repo = ShiftRepository(db)
        self.employee_repo = EmployeeRepository(db)
        self.recommendation_repo = RecommendationRepository(db)
    
    def learn_all_preferences(
        self,
        lookback_months: int = 3,
        min_samples: int = 5
    ) -> Dict[int, LearnedPreferences]:
        """
        Analyze historical shift assignments to learn preferences for all employees.
        
        Updates the assignment_preferences table with learned scores.
        
        Args:
            lookback_months: How many months of history to analyze
            min_samples: Minimum assignments needed to establish a preference
            
        Returns:
            Dictionary mapping employee_id to their learned preferences
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=30 * lookback_months)
        
        logger.info(f"🧠 Learning employee preferences from {start_date} to {end_date}")
        
        employees = self.employee_repo.get_active_employees()
        all_preferences = {}
        updates_count = 0
        
        for employee in employees:
            # Learn shift type preferences
            shift_type_prefs = self._learn_shift_type_preferences(
                employee.id, start_date, end_date, min_samples
            )
            
            # Learn day of week preferences
            day_prefs = self._learn_day_preferences(
                employee.id, start_date, end_date, min_samples
            )
            
            # Learn colleague co-assignment patterns (who they often work with)
            colleague_prefs = self._learn_colleague_preferences(
                employee.id, start_date, end_date, min_samples
            )
            
            all_preferences[employee.id] = LearnedPreferences({
                "employee_id": employee.id,
                "employee_name": f"{employee.first_name} {employee.last_name}",
                "shift_type_preferences": shift_type_prefs,
                "day_preferences": day_prefs,
                "preferred_colleagues": colleague_prefs,
                "total_assignments_analyzed": self._count_assignments(employee.id, start_date, end_date)
            })
            
            # Update database with shift type preferences
            for shift_type, score in shift_type_prefs.items():
                self.recommendation_repo.update_preference(employee.id, shift_type, score)
                updates_count += 1
        
        self.db.commit()
        
        logger.info(f"✓ Learned preferences for {len(employees)} employees ({updates_count} preference records updated)")
        return all_preferences
    
    def get_employee_preferences(
        self,
        employee_id: int,
        lookback_months: int = 3
    ) -> LearnedPreferences:
        """Get learned preferences for a specific employee"""
        end_date = date.today()
        start_date = end_date - timedelta(days=30 * lookback_months)
        
        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            return LearnedPreferences({"error": "Employee not found"})
        
        shift_type_prefs = self._learn_shift_type_preferences(employee_id, start_date, end_date, min_samples=3)
        day_prefs = self._learn_day_preferences(employee_id, start_date, end_date, min_samples=3)
        colleague_prefs = self._learn_colleague_preferences(employee_id, start_date, end_date, min_samples=3)
        
        return LearnedPreferences({
            "employee_id": employee_id,
            "employee_name": f"{employee.first_name} {employee.last_name}",
            "shift_type_preferences": shift_type_prefs,
            "day_preferences": day_prefs,
            "preferred_colleagues": colleague_prefs,
            "total_assignments_analyzed": self._count_assignments(employee_id, start_date, end_date),
            "analysis_period": {
                "start_date": str(start_date),
                "end_date": str(end_date)
            }
        })
    
    def _learn_shift_type_preferences(
        self,
        employee_id: int,
        start_date: date,
        end_date: date,
        min_samples: int
    ) -> Dict[str, float]:
        """
        Learn which shift types (morning, afternoon, evening, night) employee prefers.
        
        Returns scores 0.0-1.0 for each shift type.
        """
        # Get all assignments for employee in period
        shift_type_counts = Counter()
        total_assignments = 0
        
        current_date = start_date
        while current_date <= end_date:
            shifts = self.db.query(Shift).filter(
                Shift.date == current_date,
                Shift.is_active == True
            ).all()
            
            for shift in shifts:
                assignments = self.assignment_repo.get_by_shift(shift.id)
                if any(a.employee_id == employee_id for a in assignments):
                    shift_type = self._categorize_shift_time(shift.start_time)
                    shift_type_counts[shift_type] += 1
                    total_assignments += 1
            
            current_date += timedelta(days=1)
        
        if total_assignments < min_samples:
            return {}  # Not enough data
        
        # Calculate preference scores (normalized frequency)
        max_count = max(shift_type_counts.values()) if shift_type_counts else 1
        preferences = {}
        
        for shift_type in ["morning", "afternoon", "evening", "night"]:
            count = shift_type_counts[shift_type]
            if count > 0:
                # Score based on frequency relative to most common type
                # Add baseline of 0.3 to avoid scores too close to 0
                preferences[shift_type] = 0.3 + 0.7 * (count / max_count)
            else:
                preferences[shift_type] = 0.2  # Low score for untried types
        
        return preferences
    
    def _learn_day_preferences(
        self,
        employee_id: int,
        start_date: date,
        end_date: date,
        min_samples: int
    ) -> Dict[str, Any]:
        """
        Learn which days of week employee is most often assigned.
        
        Returns preference scores and patterns.
        """
        day_counts = Counter()
        total_assignments = 0
        
        current_date = start_date
        while current_date <= end_date:
            shifts = self.db.query(Shift).filter(
                Shift.date == current_date,
                Shift.is_active == True
            ).all()
            
            for shift in shifts:
                assignments = self.assignment_repo.get_by_shift(shift.id)
                if any(a.employee_id == employee_id for a in assignments):
                    day_of_week = current_date.weekday()
                    day_counts[day_of_week] += 1
                    total_assignments += 1
            
            current_date += timedelta(days=1)
        
        if total_assignments < min_samples:
            return {"pattern": "insufficient_data", "scores": {}}
        
        # Calculate scores
        max_count = max(day_counts.values()) if day_counts else 1
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        scores = {}
        for day_num in range(7):
            count = day_counts[day_num]
            scores[day_names[day_num]] = {
                "score": 0.3 + 0.7 * (count / max_count) if count > 0 else 0.2,
                "assignments": count
            }
        
        # Identify pattern
        weekday_count = sum(day_counts[i] for i in range(5))
        weekend_count = sum(day_counts[i] for i in range(5, 7))
        
        if weekend_count > weekday_count * 1.5:
            pattern = "weekend_preference"
        elif weekday_count > weekend_count * 1.5:
            pattern = "weekday_preference"
        else:
            pattern = "balanced"
        
        return {
            "pattern": pattern,
            "scores": scores,
            "total_assignments": total_assignments
        }
    
    def _learn_colleague_preferences(
        self,
        employee_id: int,
        start_date: date,
        end_date: date,
        min_samples: int
    ) -> List[Dict[str, Any]]:
        """
        Identify which colleagues this employee often works with.
        
        Returns list of colleagues ordered by co-assignment frequency.
        """
        colleague_counts = Counter()
        
        current_date = start_date
        while current_date <= end_date:
            shifts = self.db.query(Shift).filter(
                Shift.date == current_date,
                Shift.is_active == True
            ).all()
            
            for shift in shifts:
                assignments = self.assignment_repo.get_by_shift(shift.id)
                employee_ids = [a.employee_id for a in assignments]
                
                if employee_id in employee_ids:
                    # Count co-workers on this shift
                    for colleague_id in employee_ids:
                        if colleague_id != employee_id:
                            colleague_counts[colleague_id] += 1
            
            current_date += timedelta(days=1)
        
        if not colleague_counts:
            return []
        
        # Get top colleagues
        preferred_colleagues = []
        for colleague_id, count in colleague_counts.most_common(5):
            colleague = self.employee_repo.get_by_id(colleague_id)
            if colleague:
                preferred_colleagues.append({
                    "employee_id": colleague_id,
                    "employee_name": f"{colleague.first_name} {colleague.last_name}",
                    "co_assignments": count,
                    "affinity_score": min(1.0, count / 20.0)  # Normalize to 0-1
                })
        
        return preferred_colleagues
    
    def _categorize_shift_time(self, start_time: time) -> str:
        """Categorize a shift by its start time"""
        hour = start_time.hour
        
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "evening"
        else:
            return "night"
    
    def _count_assignments(
        self,
        employee_id: int,
        start_date: date,
        end_date: date
    ) -> int:
        """Count total assignments for employee in period"""
        count = 0
        current_date = start_date
        
        while current_date <= end_date:
            shifts = self.db.query(Shift).filter(
                Shift.date == current_date,
                Shift.is_active == True
            ).all()
            
            for shift in shifts:
                assignments = self.assignment_repo.get_by_shift(shift.id)
                if any(a.employee_id == employee_id for a in assignments):
                    count += 1
            
            current_date += timedelta(days=1)
        
        return count

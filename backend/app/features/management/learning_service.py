"""
Learning Service - Analyze historical patterns for schedule optimization
Phase 4 - US-4.2: Dynamic Optimization with Learning
"""
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, time, datetime, timedelta
from collections import defaultdict
import logging

from ...models.analytics import ActivityLog
from ...models.shift import Shift
from ...models.employee import Employee
from ...repositories.shift_repository import ShiftAssignmentRepository, ShiftRepository

logger = logging.getLogger(__name__)


class LearnedPattern(Dict[str, Any]):
    """Container for learned scheduling patterns"""
    pass


class WorkloadPrediction(Dict[str, Any]):
    """Predicted workload for a specific time period"""
    pass


class LearningService:
    """Analyze historical data to identify scheduling patterns and optimize future schedules"""
    
    def __init__(self, db: Session):
        self.db = db
        self.assignment_repo = ShiftAssignmentRepository(db)
        self.shift_repo = ShiftRepository(db)
    
    def analyze_historical_patterns(
        self,
        lookback_months: int = 3
    ) -> LearnedPattern:
        """
        Analyze historical scheduling and activity data to identify patterns.
        
        Returns learned patterns including:
        - Optimal staffing by day of week and hour
        - Busy periods and slow periods
        - Workload trends
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=30 * lookback_months)
        
        logger.info(f"📚 Analyzing historical patterns from {start_date} to {end_date}")
        
        patterns = LearnedPattern()
        
        # Pattern 1: Staffing needs by day of week and time
        patterns["staffing_by_day_hour"] = self._analyze_staffing_patterns(start_date, end_date)
        
        # Pattern 2: Workload trends
        patterns["workload_trends"] = self._analyze_workload_trends(start_date, end_date)
        
        # Pattern 3: Day of week patterns
        patterns["day_of_week_patterns"] = self._analyze_day_patterns(start_date, end_date)
        
        # Pattern 4: Coverage quality metrics
        patterns["historical_quality"] = self._analyze_coverage_quality(start_date, end_date)
        
        patterns["metadata"] = {
            "analyzed_period_start": str(start_date),
            "analyzed_period_end": str(end_date),
            "total_days": (end_date - start_date).days,
            "generated_at": datetime.now().isoformat()
        }
        
        logger.info(f"✓ Pattern analysis complete")
        return patterns
    
    def predict_optimal_staffing(
        self,
        target_date: date,
        hour: int
    ) -> WorkloadPrediction:
        """
        Predict optimal staffing level for a specific date and hour.
        
        Based on historical patterns for similar days.
        """
        # Get historical patterns
        patterns = self.analyze_historical_patterns(lookback_months=3)
        
        day_of_week = target_date.weekday()
        
        # Get average staffing for this day/hour from patterns
        staffing_patterns = patterns["staffing_by_day_hour"]
        key = f"day_{day_of_week}_hour_{hour}"
        
        if key in staffing_patterns:
            historical = staffing_patterns[key]
            
            return WorkloadPrediction({
                "target_date": str(target_date),
                "hour": hour,
                "recommended_employees": round(historical["avg_employees"]),
                "min_recommended": max(1, round(historical["min_employees"])),
                "max_recommended": round(historical["max_employees"]),
                "confidence": historical["confidence"],
                "based_on_samples": historical["sample_count"],
                "explanation": f"Based on {historical['sample_count']} similar {target_date.strftime('%A')}s at {hour}:00"
            })
        
        # Fallback to broader day-of-week pattern
        day_patterns = patterns["day_of_week_patterns"]
        if day_of_week in day_patterns:
            day_avg = day_patterns[day_of_week]["avg_employees_per_hour"]
            return WorkloadPrediction({
                "target_date": str(target_date),
                "hour": hour,
                "recommended_employees": round(day_avg),
                "min_recommended": max(1, round(day_avg * 0.8)),
                "max_recommended": round(day_avg * 1.2),
                "confidence": 0.5,
                "based_on_samples": day_patterns[day_of_week]["sample_count"],
                "explanation": f"Based on average for {target_date.strftime('%A')}s"
            })
        
        # Ultimate fallback
        return WorkloadPrediction({
            "target_date": str(target_date),
            "hour": hour,
            "recommended_employees": 2,
            "min_recommended": 1,
            "max_recommended": 3,
            "confidence": 0.3,
            "based_on_samples": 0,
            "explanation": "Insufficient historical data, using default estimate"
        })
    
    def identify_optimization_opportunities(
        self,
        schedule_id: int
    ) -> List[Dict[str, Any]]:
        """
        Compare current schedule against learned patterns to identify improvements.
        
        Returns list of optimization suggestions.
        """
        opportunities = []
        
        # Get shifts from schedule
        shifts = self.shift_repo.get_by_schedule(schedule_id)
        if not shifts:
            return opportunities
        
        # Get learned patterns
        patterns = self.analyze_historical_patterns()
        
        # Check each shift against learned optimal staffing
        for shift in shifts:
            prediction = self.predict_optimal_staffing(shift.date, shift.start_time.hour)
            
            assignments = self.assignment_repo.get_by_shift(shift.id)
            current_staffing = len(assignments)
            recommended = prediction["recommended_employees"]
            
            # Identify over/under-staffing
            if current_staffing < recommended - 1:
                opportunities.append({
                    "type": "understaffing",
                    "shift_id": shift.id,
                    "shift_date": str(shift.date),
                    "shift_time": str(shift.start_time),
                    "current_employees": current_staffing,
                    "recommended_employees": recommended,
                    "confidence": prediction["confidence"],
                    "impact": "high" if abs(current_staffing - recommended) > 1 else "medium",
                    "suggestion": f"Add {recommended - current_staffing} more employee(s) to match historical optimal staffing"
                })
            elif current_staffing > recommended + 1:
                opportunities.append({
                    "type": "overstaffing",
                    "shift_id": shift.id,
                    "shift_date": str(shift.date),
                    "shift_time": str(shift.start_time),
                    "current_employees": current_staffing,
                    "recommended_employees": recommended,
                    "confidence": prediction["confidence"],
                    "impact": "medium",
                    "suggestion": f"Reduce by {current_staffing - recommended} employee(s) based on historical patterns"
                })
        
        return opportunities
    
    def _analyze_staffing_patterns(
        self,
        start_date: date,
        end_date: date
    ) -> Dict[str, Dict[str, Any]]:
        """Analyze average staffing levels by day of week and hour"""
        patterns = {}
        
        # Get all shifts in period
        current_date = start_date
        day_hour_staffing = defaultdict(list)
        
        while current_date <= end_date:
            shifts = self.db.query(Shift).filter(
                Shift.date == current_date,
                Shift.is_active == True
            ).all()
            
            for shift in shifts:
                assignments = self.assignment_repo.get_by_shift(shift.id)
                staff_count = len(assignments)
                
                day_of_week = current_date.weekday()
                hour = shift.start_time.hour
                key = f"day_{day_of_week}_hour_{hour}"
                
                day_hour_staffing[key].append(staff_count)
            
            current_date += timedelta(days=1)
        
        # Calculate statistics
        for key, values in day_hour_staffing.items():
            if values:
                patterns[key] = {
                    "avg_employees": sum(values) / len(values),
                    "min_employees": min(values),
                    "max_employees": max(values),
                    "sample_count": len(values),
                    "confidence": min(1.0, len(values) / 10.0)  # More samples = higher confidence
                }
        
        return patterns
    
    def _analyze_workload_trends(
        self,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """Analyze workload from activity logs"""
        # Query activity logs
        logs = self.db.query(ActivityLog).filter(
            ActivityLog.date >= start_date,
            ActivityLog.date <= end_date
        ).all()
        
        if not logs:
            return {"average_workload": 0, "peak_hours": [], "slow_hours": []}
        
        # Analyze by hour
        hourly_workload = defaultdict(list)
        for log in logs:
            hourly_workload[log.hour].append(log.actual_workload_metric)
        
        # Calculate averages
        hourly_avg = {
            hour: sum(values) / len(values)
            for hour, values in hourly_workload.items()
        }
        
        overall_avg = sum(hourly_avg.values()) / len(hourly_avg) if hourly_avg else 0
        
        # Identify peak and slow hours
        peak_hours = [hour for hour, avg in hourly_avg.items() if avg > overall_avg * 1.3]
        slow_hours = [hour for hour, avg in hourly_avg.items() if avg < overall_avg * 0.7]
        
        return {
            "average_workload": overall_avg,
            "hourly_averages": hourly_avg,
            "peak_hours": sorted(peak_hours),
            "slow_hours": sorted(slow_hours),
            "total_samples": len(logs)
        }
    
    def _analyze_day_patterns(
        self,
        start_date: date,
        end_date: date
    ) -> Dict[int, Dict[str, Any]]:
        """Analyze patterns by day of week"""
        day_patterns = defaultdict(lambda: {"total_employees": 0, "sample_count": 0})
        
        current_date = start_date
        while current_date <= end_date:
            day_of_week = current_date.weekday()
            shifts = self.db.query(Shift).filter(
                Shift.date == current_date,
                Shift.is_active == True
            ).all()
            
            total_staff = sum(len(self.assignment_repo.get_by_shift(s.id)) for s in shifts)
            
            day_patterns[day_of_week]["total_employees"] += total_staff
            day_patterns[day_of_week]["sample_count"] += 1
            
            current_date += timedelta(days=1)
        
        # Calculate averages
        result = {}
        for day, data in day_patterns.items():
            if data["sample_count"] > 0:
                result[day] = {
                    "avg_employees_per_hour": data["total_employees"] / data["sample_count"],
                    "sample_count": data["sample_count"]
                }
        
        return result
    
    def _analyze_coverage_quality(
        self,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """Analyze how well shifts were covered historically"""
        total_shifts = 0
        fully_covered = 0
        under_staffed = 0
        over_staffed = 0
        
        current_date = start_date
        while current_date <= end_date:
            shifts = self.db.query(Shift).filter(
                Shift.date == current_date,
                Shift.is_active == True
            ).all()
            
            for shift in shifts:
                total_shifts += 1
                assignments = self.assignment_repo.get_by_shift(shift.id)
                staff_count = len(assignments)
                
                if staff_count >= shift.min_employees and staff_count <= shift.max_employees:
                    fully_covered += 1
                elif staff_count < shift.min_employees:
                    under_staffed += 1
                else:
                    over_staffed += 1
            
            current_date += timedelta(days=1)
        
        return {
            "total_shifts_analyzed": total_shifts,
            "coverage_rate": fully_covered / total_shifts if total_shifts > 0 else 0,
            "understaffing_rate": under_staffed / total_shifts if total_shifts > 0 else 0,
            "overstaffing_rate": over_staffed / total_shifts if total_shifts > 0 else 0
        }

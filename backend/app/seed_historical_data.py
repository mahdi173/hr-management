"""
Generate synthetic historical data for AI learning features.
Creates 6 months of realistic shift assignments with patterns.
"""
import random
from datetime import datetime, date, time, timedelta
from sqlalchemy.orm import Session
from typing import List, Dict
import logging

from .database import SessionLocal, engine
from .models.base import Base
from .models.employee import Employee
from .models.role import Role
from .models.shift import Shift
from .models.schedule import Schedule
from .models.absence import Absence, AbsenceType
from .models.availability import Availability
from .models.analytics import ActivityLog
from .repositories.shift_repository import ShiftAssignmentRepository

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class HistoricalDataGenerator:
    """Generate realistic historical shift data with learnable patterns"""
    
    def __init__(self, db: Session):
        self.db = db
        self.assignment_repo = ShiftAssignmentRepository(db)
        
        # Employee preferences (to embed patterns)
        self.employee_shift_preferences = {}  # employee_id -> preferred shift times
        self.employee_day_preferences = {}    # employee_id -> preferred days
        
    def generate_all(self, months: int = 6):
        """Generate complete historical dataset"""
        logger.info(f"🎬 Starting generation of {months} months of historical data...")
        
        # 1. Load existing employees and roles
        employees = self.db.query(Employee).filter(Employee.is_active == True).all()
        roles = self.db.query(Role).all()
        
        if len(employees) < 10:
            logger.warning(f"⚠️  Only {len(employees)} employees found. Generating more demo employees...")
            employees = self._generate_demo_employees(target_count=15)
        
        logger.info(f"✓ Using {len(employees)} employees")
        
        # 2. Generate employee preferences (to create learnable patterns)
        self._generate_employee_preferences(employees)
        
        # 3. Generate historical schedules and shifts
        end_date = date.today() - timedelta(days=7)  # Stop 1 week ago
        start_date = end_date - timedelta(days=30 * months)
        
        logger.info(f"📅 Generating schedules from {start_date} to {end_date}")
        
        total_assignments = 0
        current_date = start_date
        
        while current_date <= end_date:
            # Generate weekly schedules
            week_start = current_date
            week_end = week_start + timedelta(days=6)
            
            schedule = self._create_schedule(week_start, week_end)
            shifts = self._create_shifts_for_week(schedule, week_start, employees)
            assignments = self._assign_employees_to_shifts(shifts, employees, week_start)
            
            total_assignments += assignments
            
            current_date = week_end + timedelta(days=1)
            
            if current_date.day == 1:  # Log progress monthly
                logger.info(f"  ✓ Generated data through {current_date.strftime('%B %Y')}")
        
        # 4. Generate activity logs (workload data)
        logger.info("📊 Generating activity logs...")
        self._generate_activity_logs(start_date, end_date)
        
        self.db.commit()
        
        logger.info(f"✅ Complete! Generated {total_assignments} shift assignments over {months} months")
        logger.info(f"   Patterns embedded: shift time preferences, day preferences, workload variations")
    
    def _generate_demo_employees(self, target_count: int = 15) -> List[Employee]:
        """Generate additional demo employees if needed"""
        first_names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason", "Isabella", "William",
                      "Mia", "James", "Charlotte", "Oliver", "Amelia"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", 
                     "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]
        
        roles = self.db.query(Role).all()
        if not roles:
            logger.error("❌ No roles found. Run seed.py first!")
            return []
        
        employees = []
        existing_count = self.db.query(Employee).count()
        
        for i in range(target_count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}{i}@demo.com"
            
            # Check if exists
            existing = self.db.query(Employee).filter(Employee.email == email).first()
            if existing:
                employees.append(existing)
                continue
            
            emp = Employee(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=f"+33{random.randint(600000000, 799999999)}",
                role_id=random.choice(roles).id,
                contract_type_id=1,  # Assume CDI exists
                is_active=True
            )
            self.db.add(emp)
            employees.append(emp)
        
        self.db.commit()
        logger.info(f"  ✓ Created {len(employees) - existing_count} new demo employees")
        return employees
    
    def _generate_employee_preferences(self, employees: List[Employee]):
        """Generate realistic preferences to embed learnable patterns"""
        shift_types = ["morning", "afternoon", "evening", "night"]
        days = [0, 1, 2, 3, 4, 5, 6]  # Monday=0, Sunday=6
        
        for emp in employees:
            # 70% of employees have a preferred shift time
            if random.random() < 0.7:
                self.employee_shift_preferences[emp.id] = random.choice(shift_types)
            
            # 60% have preferred days (e.g., prefer weekdays or weekends)
            if random.random() < 0.6:
                if random.random() < 0.7:
                    # Prefer weekdays
                    self.employee_day_preferences[emp.id] = [0, 1, 2, 3, 4]
                else:
                    # Prefer weekends
                    self.employee_day_preferences[emp.id] = [5, 6]
        
        logger.info(f"  ✓ Generated preferences for {len(self.employee_shift_preferences)} employees")
    
    def _create_schedule(self, start_date: date, end_date: date) -> Schedule:
        """Create a schedule for the week"""
        from .models.schedule import ScheduleStatus
        schedule = Schedule(
            name=f"Week {start_date.strftime('%Y-W%U')}",
            start_date=start_date,
            end_date=end_date,
            status=ScheduleStatus.PUBLISHED,
            created_by_id=1  # Assume admin
        )
        self.db.add(schedule)
        self.db.flush()
        return schedule
    
    def _create_shifts_for_week(self, schedule: Schedule, week_start: date, 
                                employees: List[Employee]) -> List[Shift]:
        """Create realistic shifts for a week"""
        shifts = []
        
        # Define shift templates (restaurant/retail pattern)
        shift_templates = [
            # Morning shifts
            {"name": "Morning", "start": time(8, 0), "end": time(12, 0), "type": "morning"},
            {"name": "Mid-Morning", "start": time(9, 0), "end": time(14, 0), "type": "morning"},
            # Afternoon shifts
            {"name": "Afternoon", "start": time(12, 0), "end": time(18, 0), "type": "afternoon"},
            {"name": "Mid-Day", "start": time(14, 0), "end": time(19, 0), "type": "afternoon"},
            # Evening shifts
            {"name": "Evening", "start": time(18, 0), "end": time(22, 0), "type": "evening"},
            {"name": "Late", "start": time(19, 0), "end": time(23, 0), "type": "evening"},
        ]
        
        # Generate shifts for each day of the week
        for day_offset in range(7):
            shift_date = week_start + timedelta(days=day_offset)
            
            # Weekends need more coverage (retail/restaurant pattern)
            shifts_per_day = 6 if shift_date.weekday() >= 5 else 4
            
            for _ in range(shifts_per_day):
                template = random.choice(shift_templates)
                
                shift = Shift(
                    schedule_id=schedule.id,
                    date=shift_date,
                    start_time=template["start"],
                    end_time=template["end"],
                    required_role_id=random.choice([r.id for r in self.db.query(Role).all()]),
                    min_employees=1,
                    max_employees=2,
                    is_active=True
                )
                shift.shift_type = template["type"]  # Store for pattern matching
                self.db.add(shift)
                shifts.append(shift)
        
        self.db.flush()
        return shifts
    
    def _assign_employees_to_shifts(self, shifts: List[Shift], employees: List[Employee], 
                                    week_start: date) -> int:
        """Assign employees to shifts following preference patterns"""
        assignment_count = 0
        
        # Track weekly hours to avoid overwork
        weekly_hours = {emp.id: 0.0 for emp in employees}
        
        for shift in shifts:
            # Determine how many employees to assign
            num_to_assign = random.randint(shift.min_employees, shift.max_employees)
            
            # Score and rank employees for this shift
            candidates = []
            for emp in employees:
                if weekly_hours[emp.id] >= 40:  # Max weekly hours
                    continue
                
                # Calculate preference match score
                score = self._calculate_assignment_score(emp, shift)
                candidates.append((emp, score))
            
            # Sort by score and pick top candidates
            candidates.sort(key=lambda x: x[1], reverse=True)
            
            for emp, score in candidates[:num_to_assign]:
                # Create assignment
                from .models.shift import ShiftAssignment
                assignment = ShiftAssignment(
                    shift_id=shift.id,
                    employee_id=emp.id
                )
                self.db.add(assignment)
                
                # Track hours
                shift_hours = (datetime.combine(date.today(), shift.end_time) - 
                             datetime.combine(date.today(), shift.start_time)).seconds / 3600
                weekly_hours[emp.id] += shift_hours
                assignment_count += 1
        
        return assignment_count
    
    def _calculate_assignment_score(self, employee: Employee, shift: Shift) -> float:
        """Calculate how good this assignment is (creates learnable patterns)"""
        score = random.random() * 0.3  # Base random component
        
        # Boost score if matches shift time preference
        if employee.id in self.employee_shift_preferences:
            if hasattr(shift, 'shift_type') and shift.shift_type == self.employee_shift_preferences[employee.id]:
                score += 0.5
        
        # Boost score if matches day preference
        if employee.id in self.employee_day_preferences:
            if shift.date.weekday() in self.employee_day_preferences[employee.id]:
                score += 0.3
        
        # Slight boost for role match
        if employee.role_id == shift.required_role_id:
            score += 0.2
        
        return score
    
    def _generate_activity_logs(self, start_date: date, end_date: date):
        """Generate activity logs with realistic business patterns"""
        current_date = start_date
        
        while current_date <= end_date:
            # Business is busier on weekends and during lunch/dinner
            is_weekend = current_date.weekday() >= 5
            
            for hour in range(8, 23):  # Business hours 8am-11pm
                # Calculate workload based on patterns
                base_workload = 50
                
                # Weekend boost
                if is_weekend:
                    base_workload *= 1.5
                
                # Lunch rush (12-14)
                if 12 <= hour <= 14:
                    base_workload *= 1.8
                
                # Dinner rush (19-21)
                if 19 <= hour <= 21:
                    base_workload *= 2.0
                
                # Add randomness
                workload = base_workload * random.uniform(0.7, 1.3)
                
                # Count scheduled employees for this hour
                shifts = self.db.query(Shift).filter(
                    Shift.date == current_date,
                    Shift.start_time <= time(hour, 0),
                    Shift.end_time > time(hour, 0)
                ).all()
                
                scheduled_count = sum(len(self.assignment_repo.get_by_shift(s.id)) for s in shifts)
                
                log = ActivityLog(
                    date=current_date,
                    hour=hour,
                    actual_workload_metric=workload,
                    scheduled_employees=scheduled_count
                )
                self.db.add(log)
            
            current_date += timedelta(days=1)
        
        logger.info(f"  ✓ Generated activity logs with lunch/dinner rush patterns")


def main():
    """Main entry point for generating historical data"""
    db = SessionLocal()
    
    try:
        generator = HistoricalDataGenerator(db)
        generator.generate_all(months=6)
        
        logger.info("\n🎉 Historical data generation complete!")
        logger.info("   You can now use this data for:")
        logger.info("   - Training preference learning models")
        logger.info("   - Demonstrating schedule optimization")
        logger.info("   - Testing AI-powered recommendations")
        
    except Exception as e:
        logger.error(f"❌ Error generating historical data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

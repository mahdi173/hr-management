"""Shift and ShiftAssignment repository - Data access layer for shifts"""

from typing import List, Optional
from datetime import date, datetime, time
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func

from .base import BaseRepository
from ..models.shift import Shift, ShiftAssignment, ShiftAssignmentStatus, AssignmentType


class ShiftRepository(BaseRepository[Shift]):
    """Repository for Shift model"""
    
    def __init__(self, db: Session):
        super().__init__(Shift, db)
    
    def get_by_schedule(
        self, 
        schedule_id: int, 
        skip: int = 0, 
        limit: int = 100,
        include_assignments: bool = False
    ) -> List[Shift]:
        """Get all shifts for a specific schedule"""
        query = self.db.query(Shift).filter(Shift.schedule_id == schedule_id)
        
        if include_assignments:
            query = query.options(joinedload(Shift.assignments))
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_date_range(
        self,
        start_date: date,
        end_date: date,
        skip: int = 0,
        limit: int = 100,
        include_assignments: bool = False
    ) -> List[Shift]:
        """Get shifts within a date range"""
        query = self.db.query(Shift).filter(
            and_(
                Shift.date >= start_date,
                Shift.date <= end_date
            )
        ).order_by(Shift.date, Shift.start_time)
        
        if include_assignments:
            query = query.options(joinedload(Shift.assignments))
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_employee(
        self,
        employee_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Shift]:
        """Get all shifts assigned to a specific employee"""
        query = self.db.query(Shift).join(ShiftAssignment).filter(
            ShiftAssignment.employee_id == employee_id
        )
        
        if start_date:
            query = query.filter(Shift.date >= start_date)
        if end_date:
            query = query.filter(Shift.date <= end_date)
        
        return query.order_by(Shift.date, Shift.start_time).offset(skip).limit(limit).all()
    
    def get_by_date(self, shift_date: date) -> List[Shift]:
        """Get all shifts for a specific date"""
        return self.db.query(Shift).filter(Shift.date == shift_date).all()
    
    def get_with_assignments(self, shift_id: int) -> Optional[Shift]:
        """Get shift with all assignments eagerly loaded"""
        return self.db.query(Shift).options(
            joinedload(Shift.assignments).joinedload(ShiftAssignment.employee)
        ).filter(Shift.id == shift_id).first()


class ShiftAssignmentRepository(BaseRepository[ShiftAssignment]):
    """Repository for ShiftAssignment model"""
    
    def __init__(self, db: Session):
        super().__init__(ShiftAssignment, db)
    
    def get_by_shift(self, shift_id: int) -> List[ShiftAssignment]:
        """Get all assignments for a specific shift"""
        return self.db.query(ShiftAssignment).filter(
            ShiftAssignment.shift_id == shift_id
        ).all()
    
    def get_by_employee(
        self, 
        employee_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[ShiftAssignment]:
        """Get all assignments for a specific employee"""
        query = self.db.query(ShiftAssignment).join(Shift).filter(
            ShiftAssignment.employee_id == employee_id
        )
        
        if start_date:
            query = query.filter(Shift.date >= start_date)
        if end_date:
            query = query.filter(Shift.date <= end_date)
        
        return query.order_by(Shift.date, Shift.start_time).all()
    
    def get_by_employee_and_shift(
        self, 
        employee_id: int, 
        shift_id: int
    ) -> Optional[ShiftAssignment]:
        """Get specific assignment for employee and shift"""
        return self.db.query(ShiftAssignment).filter(
            and_(
                ShiftAssignment.employee_id == employee_id,
                ShiftAssignment.shift_id == shift_id
            )
        ).first()
    
    def check_employee_conflict(
        self,
        employee_id: int,
        shift_date: date,
        start_time: time,
        end_time: time,
        exclude_shift_id: Optional[int] = None
    ) -> bool:
        """Check if employee has overlapping shift assignment"""
        query = self.db.query(ShiftAssignment).join(Shift).filter(
            and_(
                ShiftAssignment.employee_id == employee_id,
                Shift.date == shift_date,
                or_(
                    # New shift starts during existing shift
                    and_(
                        Shift.start_time <= start_time,
                        Shift.end_time > start_time
                    ),
                    # New shift ends during existing shift
                    and_(
                        Shift.start_time < end_time,
                        Shift.end_time >= end_time
                    ),
                    # New shift completely contains existing shift
                    and_(
                        Shift.start_time >= start_time,
                        Shift.end_time <= end_time
                    )
                )
            )
        )
        
        if exclude_shift_id:
            query = query.filter(Shift.id != exclude_shift_id)
        
        return query.first() is not None
    
    def get_hours_by_employee_and_period(
        self,
        employee_id: int,
        start_date: date,
        end_date: date
    ) -> dict:
        """Calculate total hours for an employee in a date range"""
        # Get all assignments in the period
        assignments = self.get_by_employee(employee_id, start_date, end_date)
        
        total_hours = 0.0
        regular_hours = 0.0
        overtime_hours = 0.0
        
        for assignment in assignments:
            shift = assignment.shift
            
            # Calculate duration in hours
            start_dt = datetime.combine(shift.date, shift.start_time)
            end_dt = datetime.combine(shift.date, shift.end_time)
            duration = (end_dt - start_dt).total_seconds() / 3600
            
            total_hours += duration
            
            if assignment.is_overtime or assignment.assignment_type == AssignmentType.OVERTIME:
                overtime_hours += duration
            else:
                regular_hours += duration
        
        return {
            "total_hours": round(total_hours, 2),
            "regular_hours": round(regular_hours, 2),
            "overtime_hours": round(overtime_hours, 2),
            "assignment_count": len(assignments)
        }
    
    def get_overtime_shifts(
        self,
        employee_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[ShiftAssignment]:
        """Get all overtime assignments for an employee"""
        query = self.db.query(ShiftAssignment).join(Shift).filter(
            and_(
                ShiftAssignment.employee_id == employee_id,
                or_(
                    ShiftAssignment.is_overtime == True,
                    ShiftAssignment.assignment_type == AssignmentType.OVERTIME
                )
            )
        )
        
        if start_date:
            query = query.filter(Shift.date >= start_date)
        if end_date:
            query = query.filter(Shift.date <= end_date)
        
        return query.order_by(Shift.date, Shift.start_time).all()
    
    def count_assignments_for_shift(self, shift_id: int) -> int:
        """Count the number of assignments for a shift"""
        return self.db.query(ShiftAssignment).filter(
            ShiftAssignment.shift_id == shift_id
        ).count()

"""
Database seeding script - creates initial data with existence checks.
Seeds are idempotent - safe to run multiple times.
"""
from sqlalchemy.orm import Session
from app.models import Role, ContractType, User, AbsenceType
from app.database import SessionLocal
import logging

logger = logging.getLogger(__name__)


def seed_roles(db: Session) -> None:
    """Seed default roles with existence checks"""
    default_roles = [
        {
            "name": "Manager",
            "description": "Team manager with full access to scheduling and personnel management",
            "permissions": {
                "can_create_schedules": True,
                "can_approve_absences": True,
                "can_manage_employees": True,
                "can_view_analytics": True
            },
            "is_active": True
        },
        {
            "name": "Team Lead",
            "description": "Team leader with limited management capabilities",
            "permissions": {
                "can_create_schedules": True,
                "can_approve_absences": False,
                "can_manage_employees": False,
                "can_view_analytics": True
            },
            "is_active": True
        },
        {
            "name": "Employee",
            "description": "Regular employee with basic access",
            "permissions": {
                "can_create_schedules": False,
                "can_approve_absences": False,
                "can_manage_employees": False,
                "can_view_analytics": False
            },
            "is_active": True
        },
        {
            "name": "Intern",
            "description": "Temporary intern with limited access",
            "permissions": {
                "can_create_schedules": False,
                "can_approve_absences": False,
                "can_manage_employees": False,
                "can_view_analytics": False
            },
            "is_active": True
        }
    ]
    
    for role_data in default_roles:
        # Check if role already exists
        existing = db.query(Role).filter(Role.name == role_data["name"]).first()
        if not existing:
            role = Role(**role_data)
            db.add(role)
            logger.info(f"✓ Created role: {role_data['name']}")
        else:
            logger.info(f"⊘ Role already exists: {role_data['name']}")
    
    db.commit()


def seed_contract_types(db: Session) -> None:
    """Seed default contract types with existence checks"""
    default_contract_types = [
        {
            "name": "CDI - Temps plein",
            "description": "Contrat à durée indéterminée, temps plein",
            "weekly_hours": 35.0,
            "max_weekly_hours": 48.0,
            "is_active": True
        },
        {
            "name": "CDD - Temps plein",
            "description": "Contrat à durée déterminée, temps plein",
            "weekly_hours": 35.0,
            "max_weekly_hours": 48.0,
            "is_active": True
        },
        {
            "name": "Temps partiel",
            "description": "Contrat à temps partiel",
            "weekly_hours": 20.0,
            "max_weekly_hours": 25.0,
            "is_active": True
        },
        {
            "name": "Stagiaire",
            "description": "Stage conventionné",
            "weekly_hours": 35.0,
            "max_weekly_hours": 35.0,
            "is_active": True
        },
        {
            "name": "Alternance",
            "description": "Contrat d'alternance (apprentissage ou professionnalisation)",
            "weekly_hours": 35.0,
            "max_weekly_hours": 35.0,
            "is_active": True
        }
    ]
    
    for contract_data in default_contract_types:
        # Check if contract type already exists
        existing = db.query(ContractType).filter(
            ContractType.name == contract_data["name"]
        ).first()
        if not existing:
            contract_type = ContractType(**contract_data)
            db.add(contract_type)
            logger.info(f"✓ Created contract type: {contract_data['name']}")
        else:
            logger.info(f"⊘ Contract type already exists: {contract_data['name']}")
    
    db.commit()


def seed_absence_types(db: Session) -> None:
    """Seed default absence types with existence checks"""
    default_absence_types = [
        {
            "name": "Vacation",
            "description": "Paid annual leave",
            "requires_approval": True,
            "is_paid": True
        },
        {
            "name": "Sick Leave",
            "description": "Medical leave",
            "requires_approval": True,
            "is_paid": True
        },
        {
            "name": "Personal Leave",
            "description": "Unpaid personal leave",
            "requires_approval": True,
            "is_paid": False
        },
        {
            "name": "Public Holiday",
            "description": "Official public holidays",
            "requires_approval": False,
            "is_paid": True
        }
    ]
    
    for type_data in default_absence_types:
        existing = db.query(AbsenceType).filter(AbsenceType.name == type_data["name"]).first()
        if not existing:
            absence_type = AbsenceType(**type_data)
            db.add(absence_type)
            logger.info(f"✓ Created absence type: {type_data['name']}")
    
    db.commit()


def seed_database() -> None:
    """
    Main seeding function - runs all seed operations.
    Safe to run multiple times (idempotent).
    """
    db = SessionLocal()
    try:
        logger.info("🌱 Starting database seeding...")
        
        # Seed in order of dependencies
        seed_roles(db)
        seed_contract_types(db)
        seed_absence_types(db)
        
        logger.info("✅ Database seeding completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error during database seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    seed_database()

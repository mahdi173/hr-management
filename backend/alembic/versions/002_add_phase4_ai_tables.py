"""Add Phase 4 AI tables: schedule_templates, activity_logs, optimization_feedback, assignment_preferences

Revision ID: 002_add_phase4_ai_tables
Revises: 001_add_shift_is_active
Create Date: 2026-06-02 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '002_add_phase4_ai_tables'
down_revision = '001_add_shift_is_active'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create schedule_templates table
    op.create_table(
        'schedule_templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('default_shifts', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('rules', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_schedule_templates_id'), 'schedule_templates', ['id'], unique=False)
    op.create_index(op.f('ix_schedule_templates_name'), 'schedule_templates', ['name'], unique=True)
    
    # Create activity_logs table (for learning workload patterns)
    op.create_table(
        'activity_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('hour', sa.Integer(), nullable=False),
        sa.Column('actual_workload_metric', sa.Float(), nullable=False),
        sa.Column('scheduled_employees', sa.Integer(), nullable=False),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_activity_logs_id'), 'activity_logs', ['id'], unique=False)
    op.create_index(op.f('ix_activity_logs_date'), 'activity_logs', ['date'], unique=False)
    
    # Create optimization_feedback table (for learning from manager feedback)
    op.create_table(
        'optimization_feedback',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('suggestion_id', sa.String(), nullable=False),
        sa.Column('manager_id', sa.Integer(), nullable=False),
        sa.Column('was_accepted', sa.Boolean(), nullable=False),
        sa.Column('feedback_notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['manager_id'], ['employees.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_optimization_feedback_id'), 'optimization_feedback', ['id'], unique=False)
    op.create_index(op.f('ix_optimization_feedback_suggestion_id'), 'optimization_feedback', ['suggestion_id'], unique=False)
    
    # Create assignment_preferences table (for learning employee preferences)
    op.create_table(
        'assignment_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('shift_type', sa.String(), nullable=False),
        sa.Column('preference_score', sa.Float(), nullable=True, server_default='0.5'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assignment_preferences_id'), 'assignment_preferences', ['id'], unique=False)
    op.create_index(op.f('ix_assignment_preferences_employee_id'), 'assignment_preferences', ['employee_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_assignment_preferences_employee_id'), table_name='assignment_preferences')
    op.drop_index(op.f('ix_assignment_preferences_id'), table_name='assignment_preferences')
    op.drop_table('assignment_preferences')
    
    op.drop_index(op.f('ix_optimization_feedback_suggestion_id'), table_name='optimization_feedback')
    op.drop_index(op.f('ix_optimization_feedback_id'), table_name='optimization_feedback')
    op.drop_table('optimization_feedback')
    
    op.drop_index(op.f('ix_activity_logs_date'), table_name='activity_logs')
    op.drop_index(op.f('ix_activity_logs_id'), table_name='activity_logs')
    op.drop_table('activity_logs')
    
    op.drop_index(op.f('ix_schedule_templates_name'), table_name='schedule_templates')
    op.drop_index(op.f('ix_schedule_templates_id'), table_name='schedule_templates')
    op.drop_table('schedule_templates')

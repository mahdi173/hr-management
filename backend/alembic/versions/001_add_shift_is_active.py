"""Add is_active field to shifts table

Revision ID: 001_add_shift_is_active
Revises: 
Create Date: 2026-06-01 10:26:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_add_shift_is_active'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add is_active column to shifts table with default value True
    op.add_column('shifts', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'))


def downgrade() -> None:
    # Remove is_active column from shifts table
    op.drop_column('shifts', 'is_active')

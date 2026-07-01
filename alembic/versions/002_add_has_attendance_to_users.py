"""Add has_attendance column to users table

Revision ID: 002
Revises: 001
Create Date: 2026-06-18 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'users',
        sa.Column('has_attendance', sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.alter_column('users', 'has_attendance', server_default=None)


def downgrade():
    op.drop_column('users', 'has_attendance')

"""Add service_id column to projects table

Revision ID: 001
Revises: 
Create Date: 2025-02-08 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('projects', sa.Column('service_id', sa.String(), nullable=True))
    op.create_foreign_key('fk_projects_service_id', 'projects', 'services', ['service_id'], ['id'])


def downgrade():
    op.drop_constraint('fk_projects_service_id', 'projects', type_='foreignkey')
    op.drop_column('projects', 'service_id')

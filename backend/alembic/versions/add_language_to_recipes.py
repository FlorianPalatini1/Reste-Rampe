"""Add language field to recipes table

Revision ID: add_language_to_recipes
Revises: 9c8f2a1b2a3b
Create Date: 2025-10-28 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_language_to_recipes'
down_revision = '9c8f2a1b2a3b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add language column to recipes table
    op.add_column('recipes', sa.Column('language', sa.String(10), nullable=False, server_default='de'))


def downgrade() -> None:
    # Remove language column from recipes table
    op.drop_column('recipes', 'language')

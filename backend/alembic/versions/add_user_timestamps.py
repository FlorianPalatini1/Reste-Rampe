"""Add timestamps to users table

Revision ID: add_user_timestamps
Revises: add_language_to_recipes
Create Date: 2025-11-03 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_user_timestamps'
down_revision = 'add_language_to_recipes'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add created_at and last_login columns to users table
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()))
    op.add_column('users', sa.Column('last_login', sa.DateTime(), nullable=True))


def downgrade() -> None:
    # Remove created_at and last_login columns from users table
    op.drop_column('users', 'last_login')
    op.drop_column('users', 'created_at')

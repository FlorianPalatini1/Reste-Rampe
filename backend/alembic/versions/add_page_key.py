"""add page_key to pages table

Revision ID: add_page_key
Revises: 9c8f2a1b2a3b
Create Date: 2025-11-03 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_page_key'
down_revision = '9c8f2a1b2a3b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add page_key column to pages table
    op.add_column('pages', sa.Column('page_key', sa.String(100), nullable=False, server_default='privacy'))
    # Remove the server default after adding the column
    op.alter_column('pages', 'page_key', server_default=None)


def downgrade() -> None:
    # Remove page_key column
    op.drop_column('pages', 'page_key')

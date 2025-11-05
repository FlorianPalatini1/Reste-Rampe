"""Add email verification fields to users table

Revision ID: add_email_verification
Revises: add_user_timestamps
Create Date: 2025-11-04 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_email_verification'
down_revision = 'add_user_timestamps'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add email verification columns to users table
    op.add_column('users', sa.Column('is_email_verified', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('email_verification_token', sa.String(255), nullable=True, unique=True))


def downgrade() -> None:
    # Remove email verification columns from users table
    op.drop_column('users', 'email_verification_token')
    op.drop_column('users', 'is_email_verified')

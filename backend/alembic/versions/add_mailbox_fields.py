"""Add mailbox management fields to users table

Revision ID: add_mailbox_fields
Revises: add_email_verification
Create Date: 2025-11-05

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_mailbox_fields'
down_revision = 'add_email_verification'
branch_labels = None
depends_on = None


def upgrade():
    """Add mailbox management columns"""
    # Check if columns already exist before adding
    with op.batch_operations.Operations.context(op.get_context()) as batch_op:
        batch_op.add_column(
            'users',
            sa.Column('mailbox_enabled', sa.Boolean(), nullable=False, server_default='0')
        )
        batch_op.add_column(
            'users',
            sa.Column('mailbox_password_hash', sa.String(255), nullable=True)
        )
        batch_op.add_column(
            'users',
            sa.Column('mailbox_quota_mb', sa.Integer(), nullable=False, server_default='5120')
        )
        batch_op.add_column(
            'users',
            sa.Column('mailbox_created_at', sa.DateTime(), nullable=True)
        )
        batch_op.add_column(
            'users',
            sa.Column('mailbox_active', sa.Boolean(), nullable=False, server_default='1')
        )


def downgrade():
    """Remove mailbox management columns"""
    with op.batch_operations.Operations.context(op.get_context()) as batch_op:
        batch_op.drop_column('users', 'mailbox_enabled')
        batch_op.drop_column('users', 'mailbox_password_hash')
        batch_op.drop_column('users', 'mailbox_quota_mb')
        batch_op.drop_column('users', 'mailbox_created_at')
        batch_op.drop_column('users', 'mailbox_active')

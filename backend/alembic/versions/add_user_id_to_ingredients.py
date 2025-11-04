"""add_user_id_to_ingredients

Revision ID: 9e8d4c5b6a7f
Revises: add_user_timestamps
Create Date: 2025-11-03

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e8d4c5b6a7f'
down_revision = 'add_user_timestamps'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add user_id column to ingredients table
    op.add_column('ingredients', sa.Column('user_id', sa.Integer(), nullable=True))
    # Add foreign key constraint
    op.create_foreign_key('fk_ingredients_user_id', 'ingredients', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint('fk_ingredients_user_id', 'ingredients', type_='foreignkey')
    op.drop_column('ingredients', 'user_id')

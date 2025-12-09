"""rename deadline to due_date in tasks

Revision ID: abdf3b654a5f
Revises: 4dc84939f4cc
Create Date: 2025-12-07 11:22:30.779450

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abdf3b654a5f'
down_revision: Union[str, Sequence[str], None] = '4dc84939f4cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('tasks', 'deadline', new_column_name='due_date')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('tasks', 'due_date', new_column_name='deadline')

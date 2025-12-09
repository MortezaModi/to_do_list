"""rename name to title

Revision ID: fd09257329f3
Revises: c3447d0c20fb
Create Date: 2025-12-06 20:37:10.645839

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd09257329f3'
down_revision: Union[str, Sequence[str], None] = 'c3447d0c20fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('projects','name', new_column_name='title')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('projects','title', new_column_name='name')

"""add updated_at column

Revision ID: 4dc84939f4cc
Revises: fd09257329f3
Create Date: 2025-12-06 20:43:26.688849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4dc84939f4cc'
down_revision: Union[str, Sequence[str], None] = 'fd09257329f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('projects',
                  sa.Column(
                      'updated_at',
                      sa.DateTime(),
                      server_default=sa.text("'1970-01-01 00:00:00'"),
                      nullable=False
                    )
                  )
    op.execute('UPDATE projects SET updated_at=NOW();')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('projects', 'updated_at')

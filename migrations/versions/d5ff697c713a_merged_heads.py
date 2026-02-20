"""merged heads

Revision ID: d5ff697c713a
Revises: 4bb2f8785604, db95913cb32b
Create Date: 2026-02-20 18:46:14.182051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5ff697c713a'
down_revision: Union[str, Sequence[str], None] = ('4bb2f8785604', 'db95913cb32b')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

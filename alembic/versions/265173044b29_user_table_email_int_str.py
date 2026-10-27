"""user table email(int->str)

Revision ID: 265173044b29
Revises: e9e3bf619ecd
Create Date: 2026-10-27 09:28:14.072094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '265173044b29'
down_revision: Union[str, Sequence[str], None] = 'e9e3bf619ecd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("users","email", existing_type=sa.Integer(), type_=sa.String(), existing_nullable=False)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("users","email", existing_type=sa.Integer(), type_=sa.String(), existing_nullable=False)
    pass

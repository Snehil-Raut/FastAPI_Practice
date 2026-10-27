"""adding content col

Revision ID: f56f11f61e1b
Revises: 20421b4b0167
Create Date: 2026-10-26 11:41:46.829693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f56f11f61e1b'
down_revision: Union[str, Sequence[str], None] = '20421b4b0167'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass

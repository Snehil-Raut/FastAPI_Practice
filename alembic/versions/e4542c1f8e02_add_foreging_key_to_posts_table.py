"""add foreging-key to posts table

Revision ID: e4542c1f8e02
Revises: b66ffa09b1a0
Create Date: 2026-10-27 08:52:30.881029

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4542c1f8e02'
down_revision: Union[str, Sequence[str], None] = 'b66ffa09b1a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    # set the link between posts and user table
                          # name of fk   , source              , refer to (other table), which col from local table
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id']
                          , remote_cols=['id'], ondelete="CASCADE")
                            # which remote col , ondelete

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass

"""bound tasks to users

Revision ID: aaaf4f3dc112
Revises: f28860b9a3b3
Create Date: 2025-03-31 16:02:11.573482

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aaaf4f3dc112'
down_revision: Union[str, None] = 'f28860b9a3b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Tasks', sa.Column('user_id', sa.Integer(), nullable=False, server_default='1'))
    op.create_foreign_key(None, 'Tasks', 'Users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Tasks', type_='foreignkey')
    op.drop_column('Tasks', 'user_id')
    # ### end Alembic commands ###

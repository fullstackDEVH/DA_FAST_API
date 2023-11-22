"""add address for aparment

Revision ID: 3827af3968ce
Revises: 6ecb548bf023
Create Date: 2023-11-22 16:36:07.428312

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3827af3968ce'
down_revision: Union[str, None] = '6ecb548bf023'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apartment', sa.Column('address', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('apartment', 'address')
    # ### end Alembic commands ###
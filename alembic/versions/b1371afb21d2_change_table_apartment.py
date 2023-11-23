"""change table apartment

Revision ID: b1371afb21d2
Revises: 3827af3968ce
Create Date: 2023-11-23 15:55:39.911931

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1371afb21d2'
down_revision: Union[str, None] = '3827af3968ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apartment', sa.Column('city', sa.String(length=255), nullable=True))
    op.drop_column('apartment', 'rate')
    op.drop_column('apartment', 'num_toilets')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apartment', sa.Column('num_toilets', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('apartment', sa.Column('rate', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('apartment', 'city')
    # ### end Alembic commands ###

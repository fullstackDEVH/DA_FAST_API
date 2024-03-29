"""address for user

Revision ID: 6ecb548bf023
Revises: 5bcfbfdc5595
Create Date: 2023-11-22 15:23:38.398802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ecb548bf023'
down_revision: Union[str, None] = '5bcfbfdc5595'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('address', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'address')
    # ### end Alembic commands ###

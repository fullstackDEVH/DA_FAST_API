"""add owner apartment and approved field

Revision ID: 14b9cde99ca5
Revises: 4cccb8621d3a
Create Date: 2023-11-29 16:40:42.023932

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14b9cde99ca5'
down_revision: Union[str, None] = '4cccb8621d3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apartment', sa.Column('is_approved', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('apartment', 'is_approved')
    # ### end Alembic commands ###

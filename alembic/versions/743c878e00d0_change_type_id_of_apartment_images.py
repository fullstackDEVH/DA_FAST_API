"""change type id of apartment images

Revision ID: 743c878e00d0
Revises: 3534408050a0
Create Date: 2023-11-12 02:21:00.132688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '743c878e00d0'
down_revision: Union[str, None] = '3534408050a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('apartment_image', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=255),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('apartment_image', 'id',
               existing_type=sa.String(length=255),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###

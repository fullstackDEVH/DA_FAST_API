"""upgrade type char of apartment name from 32 to 255

Revision ID: b2d3ad1e8ea9
Revises: 597201d659dc
Create Date: 2023-12-04 00:19:07.793278

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2d3ad1e8ea9'
down_revision: Union[str, None] = '597201d659dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('apartment', 'name',
               existing_type=sa.VARCHAR(length=42),
               type_=sa.String(length=255),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('apartment', 'name',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=42),
               existing_nullable=False)
    # ### end Alembic commands ###

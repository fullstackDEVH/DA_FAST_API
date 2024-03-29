"""change type col system role

Revision ID: 3bc945a60908
Revises: e595b8efd939
Create Date: 2023-11-12 13:30:41.546702

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bc945a60908'
down_revision: Union[str, None] = 'e595b8efd939'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'system_role',
               existing_type=sa.VARCHAR(length=52),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'system_role',
               existing_type=sa.VARCHAR(length=52),
               nullable=False)
    # ### end Alembic commands ###

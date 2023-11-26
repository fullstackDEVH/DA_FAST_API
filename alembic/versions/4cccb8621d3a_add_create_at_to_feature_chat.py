"""add create at to feature chat

Revision ID: 4cccb8621d3a
Revises: 6ce6e3dbb8fd
Create Date: 2023-11-27 02:52:56.297048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cccb8621d3a'
down_revision: Union[str, None] = '6ce6e3dbb8fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('members_room', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('members_room', sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('message', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('message', sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('room', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('room', sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('room', 'updated_at')
    op.drop_column('room', 'created_at')
    op.drop_column('message', 'updated_at')
    op.drop_column('message', 'created_at')
    op.drop_column('members_room', 'updated_at')
    op.drop_column('members_room', 'created_at')
    # ### end Alembic commands ###
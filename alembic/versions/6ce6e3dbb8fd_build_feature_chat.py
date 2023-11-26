"""build feature chat

Revision ID: 6ce6e3dbb8fd
Revises: 19673f634489
Create Date: 2023-11-27 02:18:23.443987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ce6e3dbb8fd'
down_revision: Union[str, None] = '19673f634489'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('room',
    sa.Column('id', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('key', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('members_room',
    sa.Column('id', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.String(length=255), nullable=True),
    sa.Column('room_id', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['room_id'], ['room.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message',
    sa.Column('id', sa.String(length=255), nullable=False),
    sa.Column('sender_id', sa.String(length=255), nullable=True),
    sa.Column('room_id', sa.String(length=255), nullable=True),
    sa.Column('content', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['room_id'], ['room.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    op.drop_table('members_room')
    op.drop_table('room')
    # ### end Alembic commands ###

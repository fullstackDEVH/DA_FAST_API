"""delete oncacade and foreignkey can is nullable

Revision ID: 19673f634489
Revises: 6ca7a5677acf
Create Date: 2023-11-26 15:22:34.435166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19673f634489'
down_revision: Union[str, None] = '6ca7a5677acf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('apartment_comment', 'user_id',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('apartment_comment', 'apartment_id',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_constraint('apartment_comment_user_id_fkey', 'apartment_comment', type_='foreignkey')
    op.drop_constraint('apartment_comment_apartment_id_fkey', 'apartment_comment', type_='foreignkey')
    op.create_foreign_key(None, 'apartment_comment', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'apartment_comment', 'apartment', ['apartment_id'], ['id'], ondelete='CASCADE')
    op.alter_column('apartment_image', 'apartment_id',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('contract', 'apartment_id',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('contract', 'user_id',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contract', 'user_id',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('contract', 'apartment_id',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('apartment_image', 'apartment_id',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.drop_constraint(None, 'apartment_comment', type_='foreignkey')
    op.drop_constraint(None, 'apartment_comment', type_='foreignkey')
    op.create_foreign_key('apartment_comment_apartment_id_fkey', 'apartment_comment', 'apartment', ['apartment_id'], ['id'])
    op.create_foreign_key('apartment_comment_user_id_fkey', 'apartment_comment', 'user', ['user_id'], ['id'])
    op.alter_column('apartment_comment', 'apartment_id',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('apartment_comment', 'user_id',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###

"""empty message

Revision ID: 914f4a260d05
Revises: 
Create Date: 2025-01-22 20:26:45.689453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '914f4a260d05'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_data',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('tg_id', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.Column('height', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('activity', sa.Integer(), nullable=False),
    sa.Column('water_goal', sa.Integer(), nullable=True),
    sa.Column('calorie_goal', sa.Integer(), nullable=True),
    sa.Column('logged_water', sa.Integer(), nullable=True),
    sa.Column('logged_calories', sa.Integer(), nullable=True),
    sa.Column('burned_calories', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('tg_id')
    )
    op.create_index(op.f('ix_user_data_user_id'), 'user_data', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_data_user_id'), table_name='user_data')
    op.drop_table('user_data')
    # ### end Alembic commands ###

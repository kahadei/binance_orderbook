"""empty message

Revision ID: cff65cb92f6c
Revises: 20e82a869e89
Create Date: 2024-02-10 22:13:47.169161

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cff65cb92f6c'
down_revision: Union[str, None] = '20e82a869e89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tradesvaluebyminute',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('trade_time', sa.DateTime(), nullable=False),
    sa.Column('market_maker', sa.String(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tradesvaluebyminute')
    # ### end Alembic commands ###

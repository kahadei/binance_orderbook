"""empty message

Revision ID: 132b9714c299
Revises: 19db1b56a50b
Create Date: 2024-02-11 23:36:34.275470

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '132b9714c299'
down_revision: Union[str, None] = '19db1b56a50b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'tradesvaluebyminute', ['trade_time'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tradesvaluebyminute', type_='unique')
    # ### end Alembic commands ###

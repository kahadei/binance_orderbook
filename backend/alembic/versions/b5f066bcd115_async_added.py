"""Async added

Revision ID: b5f066bcd115
Revises: cbfd66bd0e6a
Create Date: 2023-11-08 01:10:35.339345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5f066bcd115'
down_revision: Union[str, None] = 'cbfd66bd0e6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('orders', 'side_type',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('orders', 'price',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('orders', 'quantity',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('trades', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('trades', 'event_type',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('trades', 'event_time',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               nullable=False)
    op.alter_column('trades', 'symbol',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('trades', 'tradeid',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('trades', 'price',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('trades', 'quantity',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('trades', 'buyer_order_id',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('trades', 'seller_order_id',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('trades', 'trade_time',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               nullable=False)
    op.alter_column('trades', 'market_maker',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_index('ix_trades_id', table_name='trades')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_trades_id', 'trades', ['id'], unique=False)
    op.alter_column('trades', 'market_maker',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('trades', 'trade_time',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               nullable=True)
    op.alter_column('trades', 'seller_order_id',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('trades', 'buyer_order_id',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('trades', 'quantity',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('trades', 'price',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('trades', 'tradeid',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('trades', 'symbol',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('trades', 'event_time',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               nullable=True)
    op.alter_column('trades', 'event_type',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('trades', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('orders', 'quantity',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('orders', 'price',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('orders', 'side_type',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('orders', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###
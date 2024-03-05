import sys
from datetime import datetime

sys.path.append('..')

from sqlalchemy.orm import relationship

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import *


class Base(DeclarativeBase):
    pass


class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[str]
    event_time: Mapped[datetime]
    symbol: Mapped[str]
    tradeid: Mapped[int] = mapped_column(BigInteger, unique=True)
    price: Mapped[float]
    quantity: Mapped[float]
    buyer_order_id: Mapped[int] = mapped_column(BigInteger)
    seller_order_id: Mapped[int] = mapped_column(BigInteger)
    trade_time: Mapped[datetime]
    market_maker: Mapped[str]


class TradesValueByMinute(Base):
    __tablename__ = "tradesvaluebyminute"
    id: Mapped[int] = mapped_column(primary_key=True)
    trade_time: Mapped[datetime] = mapped_column(unique=True)
    sell_quantity: Mapped[float]
    buy_quantity: Mapped[float]
    sell_trades_count: Mapped[int]
    sell_average_price: Mapped[float]
    buy_trades_count: Mapped[int]
    buy_average_price: Mapped[float]


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    side_type: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[float]


class ValueStat(Base):
    __tablename__ = "statvaluebymin"
    id: Mapped[int] = mapped_column(primary_key=True)
    trade_time: Mapped[datetime] = mapped_column(unique=True)
    quantity: Mapped[float]
    num_of_trades: Mapped[int]
    price: Mapped[float]

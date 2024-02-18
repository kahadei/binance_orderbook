import statistics
import sys

sys.path.append('')

from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
import json
import asyncio
import websockets
from pprint import pprint
from db import engine, SessionLocal
from models import Trade, Order, TradesValueByMinute


async def trade_by_min(time, trade_data):
    quantity, price, side = trade_data
    print('FFFFFF', quantity, side)
    async with SessionLocal() as session:
        try:
            stmt = await session.execute(select(TradesValueByMinute).where(TradesValueByMinute.trade_time == time))
            trade_time_obj = stmt.scalars().first()
            if trade_time_obj is None:
                trade_time_obj = TradesValueByMinute()
                trade_time_obj.trade_time = time

                if side == "SELL":
                    trade_time_obj.sell_quantity = quantity
                    trade_time_obj.sell_trades_count = 1
                    trade_time_obj.sell_average_price = price
                    trade_time_obj.buy_average_price = 0
                    trade_time_obj.buy_quantity = 0
                    trade_time_obj.buy_trades_count = 0
                elif side == "BUY":
                    trade_time_obj.buy_quantity = quantity
                    trade_time_obj.buy_average_price = price
                    trade_time_obj.buy_trades_count = 1
                    trade_time_obj.sell_trades_count = 0
                    trade_time_obj.sell_quantity = 0
                    trade_time_obj.sell_average_price = 0
            else:
                if side == "SELL":
                    prev_sell_quantity = trade_time_obj.sell_quantity
                    new_quantity = prev_sell_quantity + quantity
                    trade_time_obj.sell_quantity = new_quantity

                    prev_average_price = trade_time_obj.sell_average_price
                    new_average_price = prev_average_price + price
                    trade_time_obj.sell_average_price = new_average_price

                    # prev_trades_count = trade_time_obj.sell_trades_count
                    # new_trades_count = prev_trades_count + 1
                    # trade_time_obj.sell_trades_count = new_trades_count

                    trade_time_obj.sell_average_price = price
                elif side == "BUY":
                    prev_buy_quantity = trade_time_obj.buy_quantity
                    new_quantity = prev_buy_quantity + quantity
                    trade_time_obj.buy_quantity = new_quantity

                    # prev_average_price = trade_time_obj.buy_average_price
                    # new_average_price = prev_average_price + price
                    # trade_time_obj.sell_average_price = new_average_price

                    prev_trades_count = trade_time_obj.buy_trades_count
                    new_trades_count = prev_trades_count + 1
                    trade_time_obj.buy_trades_count = new_trades_count

                    trade_time_obj.buy_average_price = price

            session.add(trade_time_obj)
            await session.commit()
            await session.flush()

        except Exception as e:
            error = str(e.__cause__)
            await session.rollback()
            raise RuntimeError(error) from e


async def get_trades():
    async with websockets.connect('wss://stream.binance.com:9443/ws/btcusdt@trade') as ws:
        async with SessionLocal() as session:
            while True:
                # ws.send(json.dumps(subscribe))
                try:
                    message = await ws.recv()
                except:
                    pass

                data = json.loads(message)
                quantity = float(data.get('q'))
                market_maker = "SELL" if data.get('m') == True else "BUY"
                trade_time = datetime.fromtimestamp(data.get('T') / 1000).replace(second=0, microsecond=0)

                try:
                    new_order = Trade()
                    new_order.event_type = data.get('e')
                    new_order.event_time = datetime.fromtimestamp(data.get('E') / 1000)
                    new_order.symbol = data.get('s')
                    new_order.tradeid = data.get('t')
                    price = float(data.get('p'))
                    new_order.price = price
                    new_order.quantity = quantity
                    new_order.buyer_order_id = data.get('b')
                    new_order.seller_order_id = data.get('a')
                    new_order.trade_time = trade_time
                    new_order.market_maker = market_maker
                    await trade_by_min(trade_time, (quantity, price, market_maker))

                    async with session.begin():
                        session.add(new_order)
                        await session.flush()
                        await session.refresh(new_order)

                except SQLAlchemyError as e:
                    error = str(e.__cause__)
                    await session.rollback()
                    # raise RuntimeError(error) from e
                finally:
                    await session.close()


async def get_orders():
    async with websockets.connect('wss://stream.binance.com:9443/ws/btcusdt@depth5@100ms') as ws:
        async with SessionLocal() as session:
            while True:
                try:
                    message = await ws.recv()
                except:
                    pass
                data = json.loads(message)
                result = []
                for k, v in data.items():
                    if k != "lastUpdateId":
                        for agr in list(zip([k] * len(v), v)):
                            result.append(agr)
                prev_last_update = 0
                if data.get('asks') and (prev_last_update != data.get('lastUpdateId')):
                    for order in result:
                        new_order = Order()
                        new_order.side_type = order[0]
                        new_order.price = float(order[1][0])
                        new_order.quantity = float(order[1][1])
                        try:
                            async with session.begin():
                                session.add(new_order)
                                await session.flush()
                                await session.refresh(new_order)
                        except SQLAlchemyError as e:
                            # error = str(e.__cause__)
                            await session.rollback()
                            # raise RuntimeError(error) from e
                        finally:
                            await session.close()

                    prev_last_update = data.get('lastUpdateId')


async def main():
    task1 = asyncio.create_task(get_trades())
    # task2 = asyncio.create_task(get_orders())
    # task3 = asyncio.create_task(trade_by_min())

    await task1
    # await task2
    # await task3


if __name__ == "__main__":
    asyncio.run(main())

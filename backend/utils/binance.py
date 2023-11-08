import sys

sys.path.append('')

from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import json
import asyncio
import websockets
from pprint import pprint
from db import engine, SessionLocal
from models import Trade, Order


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
                new_order = Trade()
                new_order.event_type = data.get('e')
                new_order.event_time = datetime.fromtimestamp(data.get('E') / 1000)
                new_order.symbol = data.get('s')
                new_order.tradeid = data.get('t')
                new_order.price = float(data.get('p'))
                new_order.quantity = float(data.get('q'))
                new_order.buyer_order_id = data.get('b')
                new_order.seller_order_id = data.get('a')
                new_order.trade_time = datetime.fromtimestamp(data.get('T') / 1000)
                new_order.market_maker = "SELL" if data.get('m') == True else "BUY"

                try:
                    async with session.begin():
                        session.add(new_order)
                        await session.flush()
                        await session.refresh(new_order)
                except SQLAlchemyError as e:
                    error = str(e.__cause__)
                    await session.rollback()
                    raise RuntimeError(error) from e
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
                            error = str(e.__cause__)
                            await session.rollback()
                            raise RuntimeError(error) from e
                        finally:
                            await session.close()

                    prev_last_update = data.get('lastUpdateId')


async def main():
    task1 = asyncio.create_task(get_trades())
    task2 = asyncio.create_task(get_orders())

    await task1
    await task2


if __name__ == "__main__":
    asyncio.run(main())

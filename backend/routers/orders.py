import models
from typing import Annotated

from sqlalchemy import select
from starlette import status
from starlette.responses import RedirectResponse
from fastapi import APIRouter, Depends, HTTPException, Path, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db import engine, SessionLocal, get_db
from models import Trade, Order, TradesValueByMinute

router = APIRouter()


class OrderRequest(BaseModel):
    side_type: str = Field(min_length=4)
    price: float = Field()
    quantity: float = Field()


@router.get("/orders")
async def all_orders(db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(Order).order_by(Order.id.desc()).limit(50))
    orders = results.scalars().all()
    return orders


@router.get("/trades")
async def all_orders(db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(Trade).order_by(Trade.id.desc()).limit(25))
    trades = results.scalars().all()
    return trades


@router.get("/trades-by-min")
async def trades_by_min(
        min_filter: str,
        db: AsyncSession = Depends(get_db)):
    min_filter = int(min_filter)
    results = await db.execute(select(TradesValueByMinute).order_by(TradesValueByMinute.trade_time.desc()).limit(min_filter))
    trades = results.scalars().all()
    return trades


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from dotenv import load_dotenv, dotenv_values
from models import Base

load_dotenv()

config = dotenv_values(".env")

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{config["DB_USER"]}:{config["DB_PASSWORD"]}@localhost/{config["DB_NAME"]}'

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(engine, autocommit=False, autoflush=False, expire_on_commit=False)


async def get_db():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


import os

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

from bot.config import BASE_DIR

engine = create_async_engine(f'sqlite+aiosqlite:///{os.path.join(BASE_DIR, "bot/database/sqlite3.db")}', echo=True)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

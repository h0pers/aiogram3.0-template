from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

from bot.config import Settings

engine = create_async_engine(Settings.DATABASE.URL, echo=True)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

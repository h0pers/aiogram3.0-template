from typing import AsyncGenerator

from sqlalchemy.ext.asyncio.session import _AsyncSessionContextManager
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncEngine, AsyncSession

from bot.config import Settings, DatabaseSettings


class Database:
    settings = DatabaseSettings()

    @classmethod
    async def engine(cls) -> AsyncEngine:
        return create_async_engine(Settings.DATABASE.URL, echo=True)

    @classmethod
    async def session_maker(cls) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(autocommit=False, autoflush=False,
                                  expire_on_commit=False, bind=await cls.engine())

    @classmethod
    async def session(cls) -> _AsyncSessionContextManager[AsyncSession]:
        return (await cls.session_maker()).begin()

    @classmethod
    async def session_generator(cls) -> AsyncGenerator:
        async with cls.session() as session:
            yield session


class Base(AsyncAttrs, DeclarativeBase):
    pass

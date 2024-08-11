import pytest

from typing import AsyncGenerator

from bot.database import Database


@pytest.fixture(scope='session')
async def db_session() -> AsyncGenerator:
    async with await Database.session() as session:
        yield session
        await session.rollback()

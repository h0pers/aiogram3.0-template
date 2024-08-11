import logging
from typing import AsyncGenerator

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.methods.create import create
from bot.database.models.user import User
from bot.misc.controllers.user import UserController


class TestUserModel:

    @classmethod
    async def create_random_user(cls, session: AsyncSession) -> User:
        faker = Faker()
        telegram_id = faker.random_int(1, 9999999999)
        await create(session, User, {
            'telegram_id': telegram_id,
            'username': [None, faker.pystr(min_chars=1, max_chars=32)][faker.random_int(0, 1)],
            'first_name': faker.pystr(min_chars=1, max_chars=64),
            'last_name': [None, faker.pystr(min_chars=1, max_chars=64)][faker.random_int(0, 1)],
            'telegram_premium': faker.boolean(),
            'language_code': faker.language_code(),
        })
        return await UserController.database.get_user(session, telegram_id=telegram_id)

    @pytest.mark.asyncio
    async def test_user_unique(self, db_session: AsyncGenerator):
        async for session in db_session:
            user = await TestUserModel.create_random_user(session)
            try:
                await create(session, User, {
                    'telegram_id': user.telegram_id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'telegram_premium': user.telegram_premium,
                    'language_code': user.language_code,
                })
                assert False
            except Exception as e:
                logging.exception(e)
                assert True



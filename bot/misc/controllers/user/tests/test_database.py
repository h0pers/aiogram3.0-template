import pytest

from typing import AsyncGenerator

from bot.database.models.tests.test_user import TestUserModel
from bot.misc.controllers.user import UserController


class TestUserDatabaseController:

    @pytest.mark.asyncio
    async def test_ban(self, db_session: AsyncGenerator):
        async for session in db_session:
            user = await TestUserModel.create_random_user(session)
            await UserController.database.ban(session, telegram_id=user.telegram_id)
            user = await UserController.database.get_user(session, telegram_id=user.telegram_id)
            assert user.is_blocked is True

    @pytest.mark.asyncio
    async def test_unban(self, db_session: AsyncGenerator):
        async for session in db_session:
            user = await TestUserModel.create_random_user(session)
            await UserController.database.ban(session, telegram_id=user.telegram_id)
            await UserController.database.unban(session, telegram_id=user.telegram_id)
            user = await UserController.database.get_user(session, telegram_id=user.telegram_id)
            assert user.is_blocked is False

    @pytest.mark.asyncio
    async def test_user_activity_status(self, db_session: AsyncGenerator):
        async for session in db_session:
            user = await TestUserModel.create_random_user(session)
            await UserController.database.change_activity_status(session, status=False, telegram_id=user.telegram_id)
            user = await UserController.database.get_user(session, telegram_id=user.telegram_id)
            assert user.is_active is False

    @pytest.mark.asyncio
    async def test_give_admin(self, db_session: AsyncGenerator):
        async for session in db_session:
            user = await TestUserModel.create_random_user(session)
            await UserController.database.give_admin(session, telegram_id=user.telegram_id)
            user = await UserController.database.get_user(session, telegram_id=user.telegram_id)
            assert user.is_admin is True

    @pytest.mark.asyncio
    async def test_claim_admin(self, db_session: AsyncGenerator):
        async for session in db_session:
            user = await TestUserModel.create_random_user(session)
            await UserController.database.give_admin(session, telegram_id=user.telegram_id)
            await UserController.database.claim_admin(session, telegram_id=user.telegram_id)
            user = await UserController.database.get_user(session, telegram_id=user.telegram_id)
            assert user.is_admin is False

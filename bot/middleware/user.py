from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select

from bot.database import Database
from bot.database.models.user import User


class UserBanMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        try:
            async with await Database.session() as session:
                query = select(User).where(User.telegram_id == event.from_user.id,
                                           User.is_blocked.is_(True))
                statement = await session.execute(query)
                statement.one()

        except NoResultFound:
            return await handler(event, data)


class UserAdminMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        try:
            async with await Database.session() as session:
                query = select(User).where(User.telegram_id == event.from_user.id,
                                           User.is_admin.is_(True))
                statement = await session.execute(query)
                statement.one()
                return await handler(event, data)
        except NoResultFound:
            pass

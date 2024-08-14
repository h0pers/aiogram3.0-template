from abc import ABC, abstractmethod
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject
from datetime import datetime

from bot.config import Settings
from bot.database import Database
from bot.database.methods.get import get
from bot.database.methods.update import update_or_create
from bot.database.models.user import User


class GatherUserDataAbstractMiddleware(BaseMiddleware, ABC):
    @classmethod
    @abstractmethod
    async def process_user_data(cls, event: TelegramObject, bot: Bot, *args, **kwargs):
        async with await Database.session() as session:
            await update_or_create(session=session,
                                   instance=User,
                                   values={
                                       'telegram_id': event.from_user.id,
                                       'username': event.from_user.username,
                                       'first_name': event.from_user.first_name,
                                       'last_name': event.from_user.last_name,
                                       'telegram_premium': event.from_user.is_premium or False,
                                       'language_code': event.from_user.language_code,
                                       'last_activity_date': datetime.now(Settings.TIMEZONE),
                                   },
                                   telegram_id=event.from_user.id
                                   )

    @classmethod
    @abstractmethod
    async def additional_data(cls, event: TelegramObject, *args, **kwargs) -> dict:
        async with await Database.session() as session:
            return {
                'user': await get(session, User, telegram_id=event.from_user.id)
            }


class GatherUserDataMiddleware(GatherUserDataAbstractMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        await self.process_user_data(event, **data)
        data.update(await self.additional_data(event))
        return await handler(event, data)

    @classmethod
    async def process_user_data(cls, event: TelegramObject, bot: Bot, *args, **kwargs):
        return await super(GatherUserDataMiddleware, cls).process_user_data(event, bot, *args, **kwargs)

    @classmethod
    async def additional_data(cls, event: TelegramObject, *args, **kwargs) -> dict:
        return await super(GatherUserDataMiddleware, cls).additional_data(event, *args, **kwargs)

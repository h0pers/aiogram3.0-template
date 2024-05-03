from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from bot.config import ADMINS_ID


class OnlyAdmin(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs):
        if str(message.from_user.id) in ADMINS_ID:
            return True

        return False


class OnlyAdminCallback(BaseFilter):
    async def __call__(self, query: CallbackQuery, *args, **kwargs):
        if str(query.from_user.id) in ADMINS_ID:
            return True

        return False

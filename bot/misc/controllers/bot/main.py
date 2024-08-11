import asyncio
import logging
import time

from datetime import timedelta
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import Message
from sqlalchemy import select

from bot.database import Database
from bot.database.models import User
from bot.misc.controllers.user import UserController


class __Controller:
    @classmethod
    async def _send_newsletter(cls, chat_id: int, message: Message, bot: Bot) -> bool:
        async with await Database.session() as session:
            try:
                await bot.copy_message(
                    chat_id=chat_id,
                    from_chat_id=message.chat.id,
                    message_id=message.message_id,
                    reply_markup=message.reply_markup,
                )
            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
                await cls._send_newsletter(chat_id, message, bot)
            except Exception as e:
                logging.exception(e)
                await UserController.database.change_activity_status(session, status=False, telegram_id=chat_id)
                return False

            await UserController.database.change_activity_status(session, status=True, telegram_id=chat_id)
            return True

    @classmethod
    async def start_newsletter(cls, message: Message, bot: Bot) -> dict:
        async with await Database.session() as session:
            start_time = time.time()
            query = select(User.telegram_id).where(User.is_admin.is_(False), User.is_blocked.is_(False))
            telegram_ids = (await session.execute(query)).scalars().all()
            successful_executed = 0
            for telegram_id in telegram_ids:
                if await cls._send_newsletter(telegram_id, message, bot):
                    successful_executed += 1
                await asyncio.sleep(0.05)

            finish_time = timedelta(seconds=round(time.time() - start_time))
            return {
                'successful_executed': successful_executed,
                'unsuccessful_executed': len(telegram_ids) - successful_executed,
                'finish_time': str(finish_time),
                'amount': len(telegram_ids),
            }


class BotController(__Controller):
    pass



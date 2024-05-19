import asyncio
import time

from typing import List
from datetime import timedelta
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import Message
from sqlalchemy import select

from bot.database.main import SessionLocal
from bot.database.models.user import User


async def get_telegram_users(**kwargs) -> List[int]:
    async with SessionLocal.begin() as session:
        query = select(User.telegram_id).filter_by(**kwargs)
        statement = await session.execute(query)
        return statement.scalars().all()


async def change_user_status(telegram_id: int, status: bool):
    async with SessionLocal.begin() as session:
        query = select(User).where(User.telegram_id == telegram_id)
        statement = await session.execute(query)
        user = statement.scalar_one()
        user.is_active = status


async def send_newsletter(chat_id: int, message: Message, bot: Bot) -> bool:
    try:
        await bot.copy_message(
            chat_id=chat_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=message.reply_markup,
        )
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        await send_newsletter(chat_id, message, bot)
    except Exception as e:
        print(e)
        await change_user_status(chat_id, False)
        return False

    await change_user_status(chat_id, True)
    return True


async def start_newsletter(message: Message, bot: Bot) -> dict:
    start_time = time.time()
    telegram_ids = await get_telegram_users(is_admin=False, is_blocked=False)
    successful_executed = 0
    for telegram_id in telegram_ids:
        if await send_newsletter(telegram_id, message, bot):
            successful_executed += 1
        await asyncio.sleep(0.05)

    finish_time = timedelta(seconds=round(start_time - time.time()))
    return {
        'successful_executed': successful_executed,
        'unsuccessful_executed': len(telegram_ids) - successful_executed,
        'finish_time': str(finish_time),
        'amount': len(telegram_ids),
    }


async def send_message_to_admins(message: str, bot: Bot):
    admins_ids = await get_telegram_users(is_admin=True, is_blocked=False)
    for admin_id in admins_ids:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=message,
            )
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            await send_message_to_admins(message, bot)
        except Exception as e:
            print(e)
            return False


async def copy_message_to_admins(message: Message, bot: Bot) -> bool:
    admins_ids = await get_telegram_users(is_admin=True, is_blocked=False)
    for admin_id in admins_ids:
        try:
            await bot.copy_message(
                chat_id=admin_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            await copy_message_to_admins(message, bot)
        except Exception as e:
            print(e)
            return False

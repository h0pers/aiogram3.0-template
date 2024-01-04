from os import environ

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers.main import get_all_routers
from bot.database.models.main import register_models

from .config import BOT_TOKEN

dp = Dispatcher(storage=MemoryStorage())


async def start_bot():
    await register_models()
    dp.include_routers(*get_all_routers())
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

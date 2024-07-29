import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from bot.handlers.main import get_all_routers
from bot.config import Settings
from bot.middleware.db_updates import CollectData, CollectCallbackData

dp = Dispatcher(storage=Settings.BOT.REDIS_STORAGE)


async def start_bot():
    load_dotenv(dotenv_path=os.path.join(Settings.BASE_DIR, '.env'))
    dp.message.outer_middleware(CollectData())
    dp.callback_query.outer_middleware(CollectCallbackData())
    dp.include_routers(*get_all_routers())
    bot = Bot(token=Settings.BOT.TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

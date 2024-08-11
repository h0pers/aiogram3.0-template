from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage

from .config import Settings
from .handlers.main import get_all_routers
from .middleware.database import GatherUserDataMiddleware
from .middleware.user import UserBanMiddleware

if Settings.DEBUG:
    storage = MemoryStorage()
else:
    storage = RedisStorage(Settings.REDIS.obj)

dp = Dispatcher(storage=storage)

dp.message.outer_middleware(GatherUserDataMiddleware())
dp.message.outer_middleware(UserBanMiddleware())
dp.callback_query.outer_middleware(GatherUserDataMiddleware())
dp.callback_query.outer_middleware(UserBanMiddleware())


async def start_bot():
    dp.include_routers(*get_all_routers())
    bot = Bot(token=Settings.BOT.TOKEN, parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

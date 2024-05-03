from aiogram import Router

from bot.middleware.db_updates import CollectData
from .start import start_router
from .callback.main import get_user_callback_router

user_router = Router()

user_router.message.middleware(CollectData())


def get_user_router() -> Router:
    user_routers = (start_router, get_user_callback_router(),)
    user_router.include_routers(*user_routers)

    return user_router

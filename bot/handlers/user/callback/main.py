from aiogram import Router

from bot.middleware.collect_data import CollectCallbackData
from .start import start_callback_router

user_callback_router = Router()
user_callback_router.callback_query.middleware(CollectCallbackData())


def get_user_callback_router() -> Router:
    user_callback_routers = (start_callback_router,)
    user_callback_router.include_routers(*user_callback_routers)

    return user_callback_router

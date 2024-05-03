from aiogram import Router

from bot.middleware.db_updates import CollectCallbackData
from .start import start_callback_router

admin_callback_router = Router()

admin_callback_router.callback_query.middleware(CollectCallbackData())


def get_admin_callback_router() -> Router:
    admin_callback_routers = (start_callback_router,)
    admin_callback_router.include_routers(*admin_callback_routers)

    return admin_callback_router

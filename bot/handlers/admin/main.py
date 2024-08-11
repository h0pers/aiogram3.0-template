from aiogram import Router

from .callback.main import get_admin_callback_router
from bot.middleware.user import UserAdminMiddleware

admin_router = Router()

admin_router.message.middleware(UserAdminMiddleware())
admin_router.callback_query.middleware(UserAdminMiddleware())


def get_admin_router() -> Router:
    admin_routers = (get_admin_callback_router(),)
    admin_router.include_routers(*admin_routers)
    return admin_router

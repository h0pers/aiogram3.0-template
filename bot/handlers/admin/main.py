from aiogram import Router
from .admin_panel import admin_panel_router
from .callback.main import get_admin_callback_router

admin_router = Router()


def get_admin_router() -> Router:
    admin_routers = (admin_panel_router, get_admin_callback_router(),)
    admin_router.include_routers(*admin_routers)
    return admin_router

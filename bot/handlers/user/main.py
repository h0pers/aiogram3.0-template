from typing import Tuple

from aiogram import Router
from .start import start_router

user_router = Router()


def get_user_router() -> Router:
    user_routers = (start_router, )
    user_router.include_routers(*user_routers)

    return user_router

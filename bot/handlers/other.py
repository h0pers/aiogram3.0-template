from aiogram import Router
from aiogram.types import Message

other_router = Router()


@other_router.message()
async def echo(message: Message) -> None:
    await message.copy_to(message.from_user.id)


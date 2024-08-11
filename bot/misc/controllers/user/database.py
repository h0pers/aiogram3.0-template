from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models.user import User


class UserDatabaseController:
    @classmethod
    async def get_user(cls, session: AsyncSession, **kwargs) -> User:
        query = select(User).filter_by(**kwargs)
        statement = await session.execute(query)
        return statement.scalar_one()

    @classmethod
    async def get_admins(cls, session: AsyncSession, **kwargs) -> Sequence[User]:
        query = select(User).filter_by(is_blocked=False, is_admin=True, **kwargs)
        statement = await session.execute(query)
        return statement.scalars().all()

    @classmethod
    async def _set_blocked_status(cls, session: AsyncSession, status: bool, **kwargs):
        query = update(User).filter_by(**kwargs).values({'is_blocked': status})
        await session.execute(query)

    @classmethod
    async def _set_user_admin_status(cls, session: AsyncSession, status: bool, **kwargs):
        query = update(User).filter_by(**kwargs).values({'is_admin': status})
        await session.execute(query)

    @classmethod
    async def ban(cls, session: AsyncSession, **kwargs):
        await cls._set_blocked_status(session, True, **kwargs)

    @classmethod
    async def unban(cls, session: AsyncSession, **kwargs):
        await cls._set_blocked_status(session, False, **kwargs)

    @classmethod
    async def give_admin(cls, session: AsyncSession, **kwargs):
        await cls._set_user_admin_status(session, True, **kwargs)

    @classmethod
    async def claim_admin(cls, session: AsyncSession, **kwargs):
        await cls._set_user_admin_status(session, False, **kwargs)

    @classmethod
    async def change_activity_status(cls, session: AsyncSession, status: bool, **kwargs):
        query = update(User).filter_by(**kwargs).values({'is_active': status})
        await session.execute(query)


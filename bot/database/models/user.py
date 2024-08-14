import datetime

from sqlalchemy import BigInteger, String, DateTime, Boolean, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.main import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id = mapped_column(BigInteger(), unique=True)
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    telegram_premium: Mapped[bool] = mapped_column(Boolean(), default=False)
    language_code: Mapped[str] = mapped_column(String(35))
    registration_date: Mapped[datetime.datetime] = mapped_column(DateTime(), server_default=func.now())
    last_activity_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),
                                                                  server_default=func.now(),
                                                                  server_onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean(), default=False)

    @hybrid_property
    def full_name(self):
        if self.last_name is None:
            return self.first_name

        return self.first_name + " " + self.last_name

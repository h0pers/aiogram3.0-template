import os

from abc import ABC
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from pytz import timezone


class SettingsAbstract(ABC):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    TIMEZONE = timezone(os.getenv('TIMEZONE'))


class RedisSettings:
    REDIS_PORT = int(os.getenv('REDIS_PORT'))
    REDIS_HOST = os.getenv('REDIS_HOST')

    @property
    def obj(self) -> Redis:
        return Redis(host=self.REDIS_HOST, port=self.REDIS_PORT)


class DatabaseSettings:
    DRIVER = 'postgresql+asyncpg'
    USER = os.getenv("POSTGRES_USER")
    PASSWORD = os.getenv("POSTGRES_PASSWORD")
    HOST = os.getenv("POSTGRES_HOST")
    DB_NAME = os.getenv("POSTGRES_DB")
    PORT = os.getenv("POSTGRES_PORT", 5432)

    @property
    def URL(self) -> str:
        return f'{self.DRIVER}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB_NAME}'


class BotSettings:
    TOKEN = os.getenv('BOT_TOKEN')

    @property
    def REDIS_STORAGE(self) -> RedisStorage:
        redis_settings = RedisSettings()
        return RedisStorage(redis_settings.obj)


class Settings(SettingsAbstract):
    DEBUG = os.getenv('DEBUG', False)
    REDIS = RedisSettings()
    DATABASE = DatabaseSettings()
    BOT = BotSettings()

import os
from abc import ABC

from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis


class SettingsAbstract(ABC):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    TIMEZONE = os.getenv('TIMEZONE')


class RedisSettings:
    REDIS_PORT = int(os.getenv('REDIS_PORT'))
    REDIS_HOST = os.getenv('REDIS_HOST')

    @property
    def REDIS(self) -> Redis:
        return Redis(host=self.REDIS_HOST, port=self.REDIS_PORT)


class DatabaseSettings:
    DRIVER = 'postgresql+asyncpg'
    USER = os.getenv("POSTGRES_USER")
    PASSWORD = os.getenv("POSTGRES_PASSWORD")
    HOST = os.getenv("POSTGRES_HOST")
    DB_NAME = os.getenv("POSTGRES_DB")

    @property
    def URL(self) -> str:
        return f'{self.DRIVER}://{self.USER}:{self.PASSWORD}@{self.HOST}/{self.DB_NAME}'


class BotSettings:
    TOKEN = os.getenv('BOT_TOKEN')

    @property
    def REDIS_STORAGE(self) -> RedisStorage:
        redis_settings = RedisSettings()
        return RedisStorage(redis_settings.REDIS)


class Settings(SettingsAbstract):
    REDIS = RedisSettings()
    DATABASE = DatabaseSettings()
    BOT = BotSettings()

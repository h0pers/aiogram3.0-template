import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

BOT_TOKEN = os.getenv('BOT_TOKEN')

DB_URL = conn_url = f'postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}/{os.getenv("POSTGRES_DB")}'

ADMINS_ID = [int(admin.strip()) for admin in os.getenv('TELEGRAM_ADMIN_ID').split(',')]

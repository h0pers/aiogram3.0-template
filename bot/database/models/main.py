from bot.database.main import engine, Base

async def register_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

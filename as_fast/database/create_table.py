import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

from as_fast.database.models import Base
from as_fast.config.cong import config

engine = create_async_engine(config.DB_URL)


async def create_database_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await create_database_tables()


if __name__ == "__main__":
    asyncio.run(main())

# from typing import AsyncGenerator

# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
# from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from pymongo import AsyncMongoClient

from .config import settings

# DATABASE_URL = settings.db_url

# Base: DeclarativeMeta = declarative_base()

# engine = create_async_engine(DATABASE_URL)
# sessionmaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with sessionmaker() as session:
#         yield session


from motor.motor_asyncio import AsyncIOMotorClient

_client = None

async def get_mongo_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(
            settings.mongo_url,
            maxPoolSize=100,  # Оптимально для большинства случаев
            minPoolSize=10,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000
        )
    return _client
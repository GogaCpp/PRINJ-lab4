from pymongo import AsyncMongoClient

from .config import settings


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
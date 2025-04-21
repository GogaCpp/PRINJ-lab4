import asyncio
from typing import Any, Callable
from functools import wraps

from fastapi import Depends
from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure

from ..config import settings
from ..core.excaption import (
    MongoNotFoundError,
    MongoInsertError,
    MongoUpdateError,
    MongoConnectionError
)
from ..database import get_mongo_client
from ..schemas.chat import ChatCreatePayload, ChatUpdatePayload


class GraphMongoService:
    COLLECTION_NAME = "chat"

    def __init__(
        self,
        mongo_client: AsyncMongoClient = Depends(get_mongo_client),
    ):
        self._mongo_db = mongo_client[settings.mongo_db]
        self._collection = self._mongo_db[self.COLLECTION_NAME]

    @staticmethod
    def ping_mongo(timeout: float = 3) -> Callable:
        def wrapper(func: Callable) -> Callable:
            @wraps(func)
            async def wrapped(self: 'GraphMongoService', *args, **kwargs) -> Any:
                try:
                    await asyncio.wait_for(self._mongo_db.command('ping'), timeout=timeout)
                    return await func(self, *args, **kwargs)
                except ConnectionFailure:
                    raise MongoConnectionError
                except asyncio.TimeoutError:
                    raise MongoConnectionError("Timeout while trying to ping MongoDB.")
            return wrapped
        return wrapper

    @ping_mongo()
    async def create(self, target_id: str, data: ChatCreatePayload) -> dict:
        dict_data = data.model_dump()
        dict_data["_id"] = target_id
        dict_data.pop("group_id", None)
        result = await self._collection.insert_one(dict_data)
        if result.acknowledged:
            created_document = await self._collection.find_one({"_id": target_id})
            return created_document
        else:
            raise MongoInsertError

    @ping_mongo()
    async def get_by_id(self, target_id: str) -> dict:
        result = await self._collection.find_one(
            {"_id": target_id}
        )
        if result is None:
            raise MongoNotFoundError(target_id)
        return result

    @ping_mongo()
    async def update(self, target_id: str, new_data: ChatUpdatePayload) -> dict:
        graph_for_update = await self.get_by_id(target_id)
        dict_data = new_data.model_dump()
        dict_data.pop("group_id", None)
        for field, value in dict_data.items():
            if value is None:
                continue
            graph_for_update.update({field: value})

        updated_document = await self._collection.find_one_and_update(
            {"_id": target_id},
            {"$set": graph_for_update},
            return_document=True
        )
        if not updated_document:
            raise MongoUpdateError(target_id)
        return updated_document

    @ping_mongo()
    async def delete(self, target_id: str) -> None:
        result = await self._collection.delete_one(
            {"_id": target_id},
        )
        if result.deleted_count == 0:
            raise MongoNotFoundError(target_id)

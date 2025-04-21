import asyncio
from typing import Any, Callable
from functools import wraps
import uuid

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
from ..schemas.chat import BaseChat, ChatCreatePayload, ChatUpdatePayload


class ChatMongoService:
    COLLECTION_NAME = "chat"

    def __init__(
        self,
        mongo_client: AsyncMongoClient = Depends(get_mongo_client),
    ):
        self._mongo_db = mongo_client[settings.mongo_db]
        self._collection = self._mongo_db[self.COLLECTION_NAME]

    # def ping_mongo(timeout: float = 3) -> Callable:
    #     def wrapper(func: Callable) -> Callable:
    #         @wraps(func)
    #         async def wrapped(self: 'ChatMongoService', *args, **kwargs) -> Any:
    #             try:
    #                 await asyncio.wait_for(self._mongo_db.command('ping'), timeout=timeout)
    #                 return await func(self, *args, **kwargs)
    #             except ConnectionFailure:
    #                 raise MongoConnectionError
    #             except asyncio.TimeoutError:
    #                 raise MongoConnectionError("Timeout while trying to ping MongoDB.")
    #         return wrapped
    #     return wrapper

    # @ping_mongo()
    async def create(self, data: ChatCreatePayload, user_id: uuid.UUID) -> dict:
        dict_data = data.model_dump()
        dict_data["creator_id"] = user_id
        result = await self._collection.insert_one(dict_data)
        if not result.acknowledged:
            raise MongoInsertError("Insert operation not acknowledged")
        created_document = await self._collection.find_one({"name": dict_data["name"]})
        created_document["creator_id"] = uuid.UUID(created_document["creator_id"])
        return created_document

    # @ping_mongo()
    async def get_by_name(self, name: str) -> dict:
        result = await self._collection.find_one(
            {"name": name}
        )
        if result is None:
            raise MongoNotFoundError(name)
        return result

    # @ping_mongo()
    async def get_chat_list(self):
        chats = self._collection.find()
        objs = []
        async for chat in chats:
            print(chat)
            objs.append(BaseChat(
                name=chat["name"],
                is_group=chat["is_group"],
                creator_id=uuid.UUID(chat.get("user_id", chat.get("creator_id")))
            ))
        print(objs)
        return objs

    # @ping_mongo()
    async def update(self, target_id: str, new_data: ChatUpdatePayload) -> dict:
        Chat_for_update = await self.get_by_name(target_id)
        dict_data = new_data.model_dump()
        for field, value in dict_data.items():
            if value is None:
                continue
            Chat_for_update.update({field: value})

        updated_document = await self._collection.find_one_and_update(
            {"_id": target_id},
            {"$set": Chat_for_update},
            return_document=True
        )
        if not updated_document:
            raise MongoUpdateError(target_id)
        return updated_document

    # @ping_mongo()
    async def delete(self, name: str) -> None:
        result = await self._collection.delete_many(
            {"name": name}
        )
        if result.deleted_count == 0:
            raise MongoNotFoundError(name)

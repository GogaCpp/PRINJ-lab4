import asyncio
import uuid

from chat.database import get_mongo_client
from chat.schemas.chat import ChatCreatePayload
from chat.services.chat_mongo import ChatMongoService


if __name__ == "__main__":
    async def create_all(
    ) -> None:
        mongo_client = await get_mongo_client()

        chat_serv = ChatMongoService(mongo_client=mongo_client)
        chat_serv.create(
            ChatCreatePayload(
                name="Prinj",
                is_group=True
            ),
            uuid.uuid1()
        )
    asyncio.run(create_all())
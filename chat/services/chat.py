import uuid
from fastapi import Depends, HTTPException, status
from sqlalchemy import select

from ..models.chat import Chat

from ..database import get_async_session

from ..schemas.chat import ChatCreatePayload, ChatUpdatePayload

from sqlalchemy.ext.asyncio import AsyncSession


class ChatService():
    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session)
    ):
        self._session = session

    async def get_chat_by_id(self, id: uuid.UUID):
        query = (
            select(Chat)
            .where(
                Chat.id == id
            )
        )
        chat = (await self._session.execute(query)).scalars().first()
        return chat

    async def get_chat_list(self):
        query = (
            select(Chat)
        )
        chats = (await self._session.execute(query)).scalars().all()
        return {"chat_list": chats}

    async def create_chat(self, chat: ChatCreatePayload, creator_id):

        exist_chat = (await self._session.execute(select(Chat).where(Chat.name == chat.name))).scalar()
        if exist_chat:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chat alredy exist")

        chat = Chat(
            name=chat.name,
            is_group=chat.is_group,
            creator_id=creator_id
        )

        self._session.add(chat)
        await self._session.commit()
        await self._session.refresh(chat)
        return chat

    async def update_chat(self, id: uuid.UUID, chat_base: ChatUpdatePayload):
        chat = await self.get_chat_by_id(id)
        if not chat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        update_data = chat_base.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(chat, key, value)

        await self._session.commit()
        return chat

    async def delete_chat(self, id: uuid.UUID):
        chat = await self.get_chat_by_id(id)

        if not chat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        await self._session.delete(chat)
        await self._session.commit()
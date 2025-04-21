from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict


class Chat(BaseModel):
    id: uuid.UUID
    name: str
    is_group: bool
    creator_id: uuid.UUID


class ChatCreatePayload(BaseModel):
    name: str
    is_group: bool


class ChatUpdatePayload(BaseModel):
    name: Optional[str]
    is_group: Optional[bool]


class BaseChat(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    id: uuid.UUID
    name: str
    is_group: bool
    creator_id: uuid.UUID


class BaseChatList(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    chat_list: list[BaseChat]

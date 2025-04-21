from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict
from typing import Optional


class User(BaseModel):
    id: uuid.UUID
    name: str
    surname: str
    password: str
    user_type_id: int


class UserCreatePayload(BaseModel):
    name: str
    surname: str
    password: str
    user_type_id: int


class UserUpdatePayload(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    password: Optional[str]
    user_type_id: Optional[int]


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    id: uuid.UUID
    name: str
    surname: str
    password: str
    user_type_id: int


class BaseUserList(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    user_list: list[BaseUser]

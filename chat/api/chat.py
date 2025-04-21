from fastapi import APIRouter, Depends, status

# from ..services.chat import ChatService
from ..services.chat_mongo import ChatMongoService
from ..schemas.chat import BaseChat, ChatCreatePayload
from ..config import oauth2_scheme
from ..services.jwt import decode_token

router = APIRouter(prefix="/chat")


@router.get("/")
async def get_list(
    token: str = Depends(oauth2_scheme),
    chat_mongo_service: ChatMongoService = Depends()
):
    return await chat_mongo_service.get_chat_list()


@router.get("/{name}", response_model=BaseChat)
async def get_chat(
    name: str,
    token: str = Depends(oauth2_scheme),
    chat_mongo_service: ChatMongoService = Depends()
):
    return await chat_mongo_service.get_by_name(name)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BaseChat)
async def create_chat(
    chat: ChatCreatePayload,
    token: str = Depends(oauth2_scheme),
    chat_mongo_service: ChatMongoService = Depends(),
):
    d_t = await decode_token(token)
    user_id = d_t["sub"]
    return await chat_mongo_service.create(chat, user_id)


@router.delete("/{name}")
async def delete_chat(
    name: str,
    token: str = Depends(oauth2_scheme),
    chat_mongo_service: ChatMongoService = Depends()
):
    return await chat_mongo_service.delete(name)

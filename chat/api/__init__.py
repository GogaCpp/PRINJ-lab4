from fastapi import APIRouter
from .chat import router as user_router


router = APIRouter()
router.include_router(user_router)

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta

from ..services.jwt import create_access_token
from ..services.user import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends()
):
    user = await user_service.auth_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await create_access_token(
        data={
            "sub": str(user.id)
        },
        expires_delta=timedelta(minutes=480)
    )
    return {"access_token": access_token, "token_type": "bearer"}
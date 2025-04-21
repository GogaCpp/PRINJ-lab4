import uuid
from fastapi import HTTPException, status
from passlib.hash import pbkdf2_sha256
from fastapi import Depends, HTTPException, status

from ..models.users import User

from ..schemas.user import UserCreatePayload, UserUpdatePayload
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session


class UserService():
    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session)
    ):
        self._session = session

    async def get_user_by_id(self, id: uuid.UUID):
        query = (
            select(User)
            .where(
                User.id == id
            )
        )
        user = (await self._session.execute(query)).scalars().first()
        return user

    async def get_user_list(self):
        query = (
            select(User)
        )
        users = (await self._session.execute(query)).scalars().all()
        return {"user_list": users}

    async def create_user(self, user: UserCreatePayload):

        login = (await self._session.execute(select(User).where(User.name == user.name))).scalar()
        if login:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User alredy exist")

        user = User(
            name=user.name,
            surname=user.surname,
            password=pbkdf2_sha256.hash(user.password),
            user_type_id=user.user_type_id
        )

        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def update_user(self, id: uuid.UUID, user_base: UserUpdatePayload):
        user = await self.get_user_by_id(id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        update_data = user_base.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(user, key, value)

        if user_base.password is not None:
            user.password = pbkdf2_sha256.hash(user_base.password)

        await self._session.commit()
        return user

    async def delete_user(self, id: uuid.UUID):
        user = await self.get_user_by_id(id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        await self._session.delete(user)
        await self._session.commit()

    async def auth_user(self, name: str, password: str):
        query = (
            select(User)
            .where(
                User.name == name
            )
        )
        user = (await self._session.execute(query)).scalars().first()
        
        if user is not None and pbkdf2_sha256.verify(password, user.password):
            return user
        return None
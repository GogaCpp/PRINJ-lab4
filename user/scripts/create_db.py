import asyncio

from user.schemas.user import UserCreatePayload

from ..models.users import User
from ..services.user import UserService
from ..database import Base, engine


if __name__ == "__main__":
    async def create_all() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        
        user_serv = UserService()

        user_serv.create_user(
            UserCreatePayload(
                name="root",
                surname="root",
                password="root",
                user_type_id=0
            )
        )
        user_serv.create_user(
            UserCreatePayload(
                name="Andrey",
                surname="Elizarov",
                password="qwerty",
                user_type_id=0
            )
        )
        user_serv.create_user(
            UserCreatePayload(
                name="I need 16",
                surname="point",
                password="pls",
                user_type_id=0
            )
        )

    asyncio.run(create_all())
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(extra='ignore')

    # # Postgre
    # db_host: str
    # db_port: int
    # db_user: str
    # db_password: str
    # db_name: str
    # algorithm: str
    # secret_key: str

    algorithm: str
    secret_key: str

    mongo_user: str
    mongo_password: str
    mongo_db: str
    mongo_host: str
    mongo_port: int

    # @property
    # def db_url(self):
    #     return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def access_token_expire(self):
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

    @property
    def mongo_url(self):
        return f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}/"


settings = Settings(
    _env_file="./chat/.env",
    _env_file_encoding="utf-8"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8001/auth/token")

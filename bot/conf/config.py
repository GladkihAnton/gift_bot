from pydantic import BaseSettings


class Settings(BaseSettings):
    ASYNC_DATABASE_URL: str


settings = Settings()

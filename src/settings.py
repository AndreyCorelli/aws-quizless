import os
from pydantic import BaseSettings, Field


STORAGE_PATH = os.path.dirname(os.path.realpath(__file__))
STORAGE_PATH = os.path.join(STORAGE_PATH, "..", "storage")


class Settings(BaseSettings):
    storage_uri: str = Field(STORAGE_PATH)
    redis_host: str = Field("localhost")
    redis_port: int = Field(6379)

    @property
    def quiz_path(self) -> str:
        return os.path.join(STORAGE_PATH, "quiz")


settings = Settings()

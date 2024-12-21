from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    PROJECT_NAME: str = "HANDILY"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    DATABASE_URL: str | None = None
    POSTGRES_SCHEMA: str | None = None
    

    @property
    def sync_database_url(self) -> str:
        if not self.DATABASE_URL:
            url = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            # if self.POSTGRES_SCHEMA:
            #     url = url + f"?currentSchema={self.POSTGRES_SCHEMA}"
            return url
        return self.DATABASE_URL

@lru_cache
def get_settings() -> Settings:
    return Settings()
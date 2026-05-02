from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SkillFit API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    debug: bool = True

    host: str = "0.0.0.0"
    port: int = 8000
    database_url: str = "sqlite:///./skillfit.db"
    admin_token: str = "skillfit-admin"
    sarvam_api_key: str | None = None
    openai_api_key: str | None = None
    allowed_origins: List[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost",
        ]
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="SKILLFIT_",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

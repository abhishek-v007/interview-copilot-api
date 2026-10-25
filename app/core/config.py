from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_ENV_FILE = _PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    """Environment-driven application settings."""

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "interview-copilot-api"
    app_env: str = "development"
    log_level: str = "INFO"

    gemini_api_key: str = Field(default="", repr=False)
    gemini_model: str = "gemini-2.0-flash"
    gemini_timeout_seconds: float = 30.0

    database_url: str = "postgresql+psycopg://user:password@localhost:5432/interview_copilot"

    @property
    def is_test(self) -> bool:
        return self.app_env.lower() == "test"


@lru_cache
def get_settings() -> Settings:
    return Settings()

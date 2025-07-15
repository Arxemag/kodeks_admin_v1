from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    POSTGRES_URL: str = "postgresql://postgres:admin@localhost:5432/kodeks_admin"
    KODEKS_BASE_URL: str = "http://suntd.kodeks.expert:1210"  # fallback значение

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / '.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()

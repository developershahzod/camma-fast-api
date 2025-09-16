import os
from typing import Any, Optional
from pydantic import PostgresDsn, field_validator, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore"
    )
    
    # App settings
    APP_NAME: str = "CAMMA API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database (Render sets DATABASE_URL automatically)
    DATABASE_URL: Optional[PostgresDsn] = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str]) -> Any:
        if isinstance(v, str) and v != "":
            return v
        # fallback to environment variables
        return PostgresDsn.build(
            scheme="postgresql",
            username=os.getenv("POSTGRES_USER", "camma_db_user"),
            password=os.getenv("POSTGRES_PASSWORD", "ikLyUadhglgN8o1CFjW6y6V9zouLMwSN"),
            host=os.getenv("POSTGRES_HOST", "dpg-d34pf7odl3ps7383eoe0-a"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            path=f"/{os.getenv('POSTGRES_DB', 'camma_db')}",
        )

    # Redis (optional)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # File storage
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    # Security
    CORS_ORIGINS: list = ["*"]

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
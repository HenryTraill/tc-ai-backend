from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = 'postgresql://postgres@localhost/tcai'

    # Redis
    redis_url: str = 'redis://localhost:6379/0'

    # API Settings
    api_host: str = '0.0.0.0'
    api_port: int = 8000
    debug: bool = False

    # CORS
    allowed_origins: str = 'http://localhost:3000,http://localhost:5173'

    # Sentry
    sentry_dsn: Optional[str] = None

    # Logfire
    logfire_token: Optional[str] = None

    class Config:
        env_file = '.env'
        case_sensitive = False


settings = Settings()

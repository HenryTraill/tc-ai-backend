from typing import Optional

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file='.env', case_sensitive=False)

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

    # JWT Authentication
    secret_key: str = 'secret'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60 * 24 * 2  # 2 days

    # Sentry
    sentry_dsn: Optional[str] = None

    # Logfire
    logfire_token: Optional[str] = None

    # Eurus
    eurus_api_url: str = 'http://localhost:5001'
    eurus_api_key: str = 'test-key'


settings = Settings()

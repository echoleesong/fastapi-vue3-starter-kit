"""应用配置管理."""
from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置类."""

    # ==================== 应用配置 ====================
    APP_NAME: str = "FastAPI Starter Kit"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: Literal["dev", "staging", "prod"] = "dev"

    # ==================== API 配置 ====================
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173"

    # ==================== 数据库配置 ====================
    DATABASE_URL: PostgresDsn
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_ECHO: bool = False

    # ==================== Redis 配置 ====================
    REDIS_URL: str = "redis://localhost:6379/0"

    # ==================== 日志配置 ====================
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    LOG_FORMAT: Literal["json", "text"] = "json"
    LOG_FILE_PATH: str = "logs/app.log"

    # ==================== 安全配置 ====================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ==================== 分页配置 ====================
    PAGINATION_MAX_SIZE: int = 100
    PAGINATION_DEFAULT_SIZE: int = 20

    @property
    def cors_origins(self) -> list[str]:
        """解析 CORS 源."""
        if not self.BACKEND_CORS_ORIGINS:
            return ["http://localhost:5173"]
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例."""
    return Settings()


settings = get_settings()

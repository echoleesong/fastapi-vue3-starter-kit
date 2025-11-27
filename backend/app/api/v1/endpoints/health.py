"""健康检查端点."""
from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    """健康检查响应."""

    status: str
    app_name: str
    version: str
    environment: str


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """健康检查端点.

    Returns:
        健康状态信息
    """
    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
    )

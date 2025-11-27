"""API v1 路由聚合."""
from fastapi import APIRouter

from app.api.v1.endpoints import health, users

api_router = APIRouter()

# 注册子路由
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])

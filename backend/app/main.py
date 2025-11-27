"""FastAPI 应用入口."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import AppException, app_exception_handler
from app.core.logging import get_logger, setup_logging
from app.middleware.correlation_id import CorrelationIdMiddleware
from app.middleware.logging_middleware import LoggingMiddleware

# 设置日志
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """应用生命周期管理."""
    # 启动
    logger.info("Application startup", app_name=settings.APP_NAME, version=settings.APP_VERSION)
    yield
    # 关闭
    logger.info("Application shutdown")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="FastAPI + Vue 3 全栈开发框架",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 自定义中间件
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(LoggingMiddleware)

# 异常处理器
app.add_exception_handler(AppException, app_exception_handler)

# 注册路由
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root() -> dict[str, str]:
    """根路径."""
    return {
        "message": "Welcome to FastAPI Starter Kit",
        "docs": "/docs",
        "version": settings.APP_VERSION,
    }

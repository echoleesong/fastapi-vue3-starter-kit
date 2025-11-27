"""请求日志中间件"""
import time
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """记录所有请求的详细信息."""

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        """处理请求.

        Args:
            request: 请求对象
            call_next: 下一个中间件

        Returns:
            响应对象
        """
        start_time = time.time()

        # 记录请求信息
        logger.info(
            "Request started",
            method=request.method,
            path=request.url.path,
            client_host=request.client.host if request.client else None,
        )

        # 处理请求
        response: Response = await call_next(request)

        # 计算处理时间
        process_time = time.time() - start_time

        # 记录响应信息
        logger.info(
            "Request completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time=f"{process_time:.3f}s",
        )

        # 添加处理时间到响应头
        response.headers["X-Process-Time"] = f"{process_time:.3f}"

        return response

"""请求追踪 ID 中间件."""
import uuid
from typing import Any

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """为每个请求生成唯一的关联 ID."""

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        """处理请求.

        Args:
            request: 请求对象
            call_next: 下一个中间件

        Returns:
            响应对象
        """
        # 从请求头获取或生成新的 request_id
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # 绑定到 structlog 上下文
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        # 将 request_id 附加到请求状态
        request.state.request_id = request_id

        # 处理请求
        response: Response = await call_next(request)

        # 在响应头中返回 request_id
        response.headers["X-Request-ID"] = request_id

        return response

"""自定义异常类和处理器."""
from typing import Any

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.logging import get_logger

logger = get_logger(__name__)


class AppException(Exception):
    """应用基础异常类."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: dict[str, Any] | None = None,
    ):
        """初始化异常.

        Args:
            code: 错误代码
            message: 错误消息
            status_code: HTTP 状态码
            details: 错误详情
        """
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundException(AppException):
    """资源未找到异常."""

    def __init__(
        self, message: str = "Resource not found", details: dict[str, Any] | None = None
    ):
        """初始化."""
        super().__init__(
            code="NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details,
        )


class ValidationException(AppException):
    """验证失败异常."""

    def __init__(
        self, message: str = "Validation failed", details: dict[str, Any] | None = None
    ):
        """初始化."""
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details,
        )


class UnauthorizedException(AppException):
    """未授权异常."""

    def __init__(self, message: str = "Unauthorized", details: dict[str, Any] | None = None):
        """初始化."""
        super().__init__(
            code="UNAUTHORIZED",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details,
        )


class ForbiddenException(AppException):
    """禁止访问异常."""

    def __init__(self, message: str = "Forbidden", details: dict[str, Any] | None = None):
        """初始化."""
        super().__init__(
            code="FORBIDDEN",
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            details=details,
        )


class ConflictException(AppException):
    """资源冲突异常."""

    def __init__(self, message: str = "Resource conflict", details: dict[str, Any] | None = None):
        """初始化."""
        super().__init__(
            code="CONFLICT",
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            details=details,
        )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """自定义异常处理器.

    Args:
        request: 请求对象
        exc: 异常实例

    Returns:
        JSON 响应
    """
    logger.error(
        "Application exception occurred",
        code=exc.code,
        message=exc.message,
        details=exc.details,
        path=request.url.path,
        method=request.method,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
                "request_id": getattr(request.state, "request_id", None),
            }
        },
    )

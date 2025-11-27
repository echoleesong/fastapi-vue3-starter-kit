"""日志系统配置."""
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import structlog
from structlog.types import EventDict, Processor

from app.core.config import settings


def add_china_timestamp(
    logger: Any, method_name: str, event_dict: EventDict
) -> EventDict:
    """添加中国时区的时间戳.

    Args:
        logger: logger 实例
        method_name: 方法名
        event_dict: 事件字典

    Returns:
        添加了时间戳的事件字典
    """
    # 使用 Asia/Shanghai 时区
    china_tz = ZoneInfo("Asia/Shanghai")
    now = datetime.now(china_tz)

    # 添加人类可读的时间戳
    event_dict["timestamp"] = now.strftime("%Y-%m-%d %H:%M:%S")
    # 保留 ISO 格式用于机器处理
    event_dict["timestamp_iso"] = now.isoformat()

    return event_dict


def setup_logging() -> None:
    """配置结构化日志系统."""
    # 确保日志目录存在
    log_path = Path(settings.LOG_FILE_PATH)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # 配置日志级别
    log_level = getattr(logging, settings.LOG_LEVEL)

    # 配置标准库 logging
    logging.basicConfig(
        format="%(message)s",
        level=log_level,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(settings.LOG_FILE_PATH),
        ],
    )

    # 配置 structlog 处理器
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        add_china_timestamp,  # 使用自定义时间戳
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # 根据格式选择渲染器
    if settings.LOG_FORMAT == "json":
        # 使用格式化的JSON渲染器，带缩进和换行
        processors.append(
            structlog.processors.JSONRenderer(
                indent=2,  # 2个空格缩进
                ensure_ascii=False,  # 支持中文字符
                sort_keys=True,  # 按键排序
            )
        )
    else:
        # 开发模式使用彩色控制台输出，包含时间戳
        processors.append(
            structlog.dev.ConsoleRenderer(
                colors=True,  # 启用颜色
                exception_formatter=structlog.dev.plain_traceback,
            )
        )

    # 配置 structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> Any:
    """获取 logger 实例.

    Args:
        name: logger 名称

    Returns:
        structlog logger 实例
    """
    return structlog.get_logger(name)

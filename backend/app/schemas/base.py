"""基础 Schema."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TimestampSchema(BaseModel):
    """时间戳 Schema."""

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginationParams(BaseModel):
    """分页参数."""

    skip: int = 0
    limit: int = 20

    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseModel):
    """分页响应."""

    total: int
    items: list[BaseModel]
    skip: int
    limit: int

    model_config = ConfigDict(from_attributes=True)

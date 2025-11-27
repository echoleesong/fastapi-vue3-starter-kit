"""用户 Schema."""
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.base import TimestampSchema


class UserBase(BaseModel):
    """用户基础 Schema."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str | None = Field(None, max_length=100)

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    """用户创建 Schema."""

    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """用户更新 Schema."""

    email: EmailStr | None = None
    username: str | None = Field(None, min_length=3, max_length=50)
    full_name: str | None = Field(None, max_length=100)
    password: str | None = Field(None, min_length=8)

    model_config = ConfigDict(from_attributes=True)


class User(UserBase, TimestampSchema):
    """用户响应 Schema."""

    id: int
    is_active: bool
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)


class UserInDB(User):
    """数据库中的用户 Schema."""

    hashed_password: str

    model_config = ConfigDict(from_attributes=True)

"""安全相关功能：JWT、密码哈希等."""
from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import UnauthorizedException

# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码.

    Args:
        plain_password: 明文密码
        hashed_password: 哈希后的密码

    Returns:
        是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希.

    Args:
        password: 明文密码

    Returns:
        哈希后的密码
    """
    return pwd_context.hash(password)


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """创建访问令牌.

    Args:
        data: 要编码的数据
        expires_delta: 过期时间

    Returns:
        JWT 令牌
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    """解码访问令牌.

    Args:
        token: JWT 令牌

    Returns:
        解码后的数据

    Raises:
        UnauthorizedException: 令牌无效或过期
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise UnauthorizedException(
            message="Could not validate credentials",
            details={"error": str(e)},
        ) from e

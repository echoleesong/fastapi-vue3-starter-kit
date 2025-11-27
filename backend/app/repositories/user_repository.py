"""用户 Repository."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """用户数据访问层."""

    def __init__(self, db: AsyncSession):
        """初始化.

        Args:
            db: 数据库会话
        """
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> User | None:
        """根据邮箱获取用户.

        Args:
            email: 邮箱地址

        Returns:
            用户实例 或 None
        """
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        """根据用户名获取用户.

        Args:
            username: 用户名

        Returns:
            用户实例 或 None
        """
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def exists_by_email(self, email: str) -> bool:
        """检查邮箱是否存在.

        Args:
            email: 邮箱地址

        Returns:
            是否存在
        """
        user = await self.get_by_email(email)
        return user is not None

    async def exists_by_username(self, username: str) -> bool:
        """检查用户名是否存在.

        Args:
            username: 用户名

        Returns:
            是否存在
        """
        user = await self.get_by_username(username)
        return user is not None

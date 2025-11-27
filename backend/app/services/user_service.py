"""用户业务逻辑服务."""
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictException, NotFoundException
from app.core.logging import get_logger
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate

logger = get_logger(__name__)


class UserService:
    """用户业务逻辑层."""

    def __init__(self, db: AsyncSession):
        """初始化.

        Args:
            db: 数据库会话
        """
        self.repository = UserRepository(db)

    async def create_user(self, user_data: UserCreate) -> User:
        """创建用户.

        Args:
            user_data: 用户创建数据

        Returns:
            创建的用户

        Raises:
            ConflictException: 邮箱或用户名已存在
        """
        # 检查邮箱是否存在
        if await self.repository.exists_by_email(user_data.email):
            logger.warning("Attempt to create user with existing email", email=user_data.email)
            raise ConflictException(
                message="Email already registered", details={"email": user_data.email}
            )

        # 检查用户名是否存在
        if await self.repository.exists_by_username(user_data.username):
            logger.warning(
                "Attempt to create user with existing username", username=user_data.username
            )
            raise ConflictException(
                message="Username already taken", details={"username": user_data.username}
            )

        # 创建用户
        hashed_password = get_password_hash(user_data.password)
        user = await self.repository.create(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
        )

        logger.info("User created successfully", user_id=user.id, username=user.username)
        return user

    async def get_user(self, user_id: int) -> User:
        """获取用户.

        Args:
            user_id: 用户 ID

        Returns:
            用户实例

        Raises:
            NotFoundException: 用户不存在
        """
        user = await self.repository.get(user_id)
        if not user:
            raise NotFoundException(message="User not found", details={"user_id": user_id})
        return user

    async def get_users(self, skip: int = 0, limit: int = 20) -> list[User]:
        """获取用户列表.

        Args:
            skip: 跳过数量
            limit: 限制数量

        Returns:
            用户列表
        """
        return await self.repository.get_multi(skip=skip, limit=limit)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """更新用户.

        Args:
            user_id: 用户 ID
            user_data: 更新数据

        Returns:
            更新后的用户

        Raises:
            NotFoundException: 用户不存在
            ConflictException: 邮箱或用户名已被其他用户使用
        """
        # 检查用户是否存在
        user = await self.get_user(user_id)

        # 准备更新数据
        update_data = user_data.model_dump(exclude_unset=True)

        # 检查邮箱冲突
        if "email" in update_data and update_data["email"] != user.email:
            if await self.repository.exists_by_email(update_data["email"]):
                raise ConflictException(
                    message="Email already in use", details={"email": update_data["email"]}
                )

        # 检查用户名冲突
        if "username" in update_data and update_data["username"] != user.username:
            if await self.repository.exists_by_username(update_data["username"]):
                raise ConflictException(
                    message="Username already taken", details={"username": update_data["username"]}
                )

        # 处理密码更新
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        # 更新用户
        updated_user = await self.repository.update(user_id, **update_data)

        logger.info("User updated successfully", user_id=user_id)
        return updated_user  # type: ignore

    async def delete_user(self, user_id: int) -> None:
        """删除用户.

        Args:
            user_id: 用户 ID

        Raises:
            NotFoundException: 用户不存在
        """
        # 检查用户是否存在
        await self.get_user(user_id)

        # 删除用户
        await self.repository.delete(user_id)
        logger.info("User deleted successfully", user_id=user_id)

    async def authenticate(self, username: str, password: str) -> User | None:
        """认证用户.

        Args:
            username: 用户名
            password: 密码

        Returns:
            认证成功返回用户，失败返回 None
        """
        user = await self.repository.get_by_username(username)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

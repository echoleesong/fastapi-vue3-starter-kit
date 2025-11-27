"""基础 Repository."""
from typing import Any, Generic, Type, TypeVar

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """基础 Repository，提供通用 CRUD 操作."""

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        """初始化.

        Args:
            model: ORM 模型类
            db: 数据库会话
        """
        self.model = model
        self.db = db

    async def get(self, id: Any) -> ModelType | None:
        """根据 ID 获取单条记录.

        Args:
            id: 记录 ID

        Returns:
            模型实例 或 None
        """
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """获取多条记录（分页）.

        Args:
            skip: 跳过数量
            limit: 限制数量

        Returns:
            模型实例列表
        """
        result = await self.db.execute(select(self.model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, **kwargs: Any) -> ModelType:
        """创建记录.

        Args:
            **kwargs: 模型字段

        Returns:
            创建的模型实例
        """
        obj = self.model(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def update(self, id: Any, **kwargs: Any) -> ModelType | None:
        """更新记录.

        Args:
            id: 记录 ID
            **kwargs: 更新字段

        Returns:
            更新后的模型实例 或 None
        """
        await self.db.execute(update(self.model).where(self.model.id == id).values(**kwargs))
        return await self.get(id)

    async def delete(self, id: Any) -> bool:
        """删除记录.

        Args:
            id: 记录 ID

        Returns:
            是否删除成功
        """
        result = await self.db.execute(delete(self.model).where(self.model.id == id))
        return result.rowcount > 0

    async def count(self) -> int:
        """计数.

        Returns:
            记录总数
        """
        result = await self.db.execute(select(func.count()).select_from(self.model))
        return result.scalar_one()

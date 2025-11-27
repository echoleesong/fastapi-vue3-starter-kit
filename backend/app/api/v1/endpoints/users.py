"""用户管理端点."""
from fastapi import APIRouter, status

from app.api.deps import DBSession
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: DBSession) -> User:
    """创建新用户.

    Args:
        user_data: 用户创建数据
        db: 数据库会话

    Returns:
        创建的用户
    """
    service = UserService(db)
    return await service.create_user(user_data)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: DBSession) -> User:
    """获取用户详情.

    Args:
        user_id: 用户 ID
        db: 数据库会话

    Returns:
        用户信息
    """
    service = UserService(db)
    return await service.get_user(user_id)


@router.get("", response_model=list[User])
async def get_users(skip: int = 0, limit: int = 20, db: DBSession = None) -> list[User]:
    """获取用户列表.

    Args:
        skip: 跳过数量
        limit: 限制数量
        db: 数据库会话

    Returns:
        用户列表
    """
    service = UserService(db)
    return await service.get_users(skip=skip, limit=limit)


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_data: UserUpdate, db: DBSession) -> User:
    """更新用户信息.

    Args:
        user_id: 用户 ID
        user_data: 更新数据
        db: 数据库会话

    Returns:
        更新后的用户
    """
    service = UserService(db)
    return await service.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: DBSession) -> None:
    """删除用户.

    Args:
        user_id: 用户 ID
        db: 数据库会话
    """
    service = UserService(db)
    await service.delete_user(user_id)

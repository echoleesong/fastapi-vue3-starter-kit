"""依赖注入."""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

# 数据库会话依赖
DBSession = Annotated[AsyncSession, Depends(get_db)]

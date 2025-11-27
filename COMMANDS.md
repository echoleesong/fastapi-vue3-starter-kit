# FastAPI Vue3 Starter Kit - 常用命令参考

本文档提供了项目开发、部署和维护过程中的常用命令。

## 目录
- [Docker 操作](#docker-操作)
- [数据库操作](#数据库操作)
- [开发命令](#开发命令)
- [生产部署](#生产部署)
- [故障排查](#故障排查)

---

## Docker 操作

### 启动服务

```bash
# 启动所有服务（开发环境）
docker-compose up -d

# 启动并重新构建镜像
docker-compose up -d --build

# 启动特定服务
docker-compose up -d backend
docker-compose up -d frontend
```

### 停止服务

```bash
# 停止所有服务
docker-compose stop

# 停止特定服务
docker-compose stop backend
docker-compose stop frontend

# 停止并删除容器
docker-compose down

# 停止并删除容器、卷、网络
docker-compose down -v
```

### 重启服务

```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart backend
docker-compose restart frontend
```

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs

# 实时查看后端日志
docker-compose logs -f backend

# 实时查看前端日志
docker-compose logs -f frontend

# 查看最近100行日志
docker-compose logs --tail=100 backend

# 查看特定时间范围的日志
docker-compose logs --since 2h backend
```

### 进入容器

```bash
# 进入后端容器的 bash
docker-compose exec backend bash

# 进入前端容器的 sh
docker-compose exec frontend sh

# 进入数据库容器
docker-compose exec db bash

# 进入 Redis 容器
docker-compose exec redis sh
```

### 查看服务状态

```bash
# 查看所有服务状态
docker-compose ps

# 查看详细信息
docker-compose ps -a

# 查看资源使用情况
docker stats
```

### 清理资源

```bash
# 清理未使用的容器
docker container prune

# 清理未使用的镜像
docker image prune

# 清理所有未使用的资源（容器、网络、镜像、卷）
docker system prune -a

# 清理并释放空间（慎用）
docker system prune -a --volumes
```

---

## 数据库操作

### 数据库迁移

```bash
# 进入后端容器
docker-compose exec backend bash

# 查看当前迁移状态
alembic current

# 查看迁移历史
alembic history

# 升级到最新版本
alembic upgrade head

# 降级一个版本
alembic downgrade -1

# 创建新的迁移文件
alembic revision --autogenerate -m "描述信息"

# 创建空白迁移文件
alembic revision -m "描述信息"
```

### 数据库连接

```bash
# 使用 psql 连接数据库
docker-compose exec db psql -U postgres -d fastapi_db

# 或者从本地连接（需要暴露端口）
psql -h localhost -p 5432 -U postgres -d fastapi_db
```

### 常用 SQL 命令

```sql
-- 列出所有数据库
\l

-- 连接到数据库
\c fastapi_db

-- 列出所有表
\dt

-- 查看表结构
\d users

-- 查看表数据
SELECT * FROM users;

-- 退出
\q
```

### 数据库备份与恢复

```bash
# 备份数据库
docker-compose exec db pg_dump -U postgres fastapi_db > backup_$(date +%Y%m%d_%H%M%S).sql

# 恢复数据库
docker-compose exec -T db psql -U postgres fastapi_db < backup_20250127.sql

# 备份到容器内
docker-compose exec db pg_dump -U postgres fastapi_db > /tmp/backup.sql

# 从容器复制备份文件
docker cp postgres-db:/tmp/backup.sql ./backup.sql
```

---

## 开发命令

### 后端开发

```bash
# 进入后端目录
cd backend

# 安装依赖（本地开发）
pip install -r requirements-dev.txt

# 代码格式化
black app/ tests/
isort app/ tests/

# 代码检查
flake8 app/ tests/
mypy app/

# 运行测试
pytest tests/ -v

# 运行测试并显示覆盖率
pytest tests/ --cov=app --cov-report=html

# 运行特定测试文件
pytest tests/test_api.py -v

# 本地运行后端（不使用 Docker）
uvicorn app.main:app --reload

# 指定端口运行
uvicorn app.main:app --reload --port 8001
```

### 前端开发

```bash
# 进入前端目录
cd frontend

# 安装依赖（本地开发）
npm install

# 本地运行前端（不使用 Docker）
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview

# 代码检查
npm run lint

# 代码格式化
npm run format

# 类型检查
npm run type-check
```

### Redis 操作

```bash
# 进入 Redis CLI
docker-compose exec redis redis-cli

# 查看所有键
KEYS *

# 获取键值
GET key_name

# 设置键值
SET key_name value

# 删除键
DEL key_name

# 清空当前数据库
FLUSHDB

# 清空所有数据库
FLUSHALL

# 查看 Redis 信息
INFO

# 退出
exit
```

---

## 生产部署

### 构建生产镜像

```bash
# 使用生产配置构建
docker-compose -f docker-compose.prod.yml build

# 不使用缓存重新构建
docker-compose -f docker-compose.prod.yml build --no-cache

# 构建特定服务
docker-compose -f docker-compose.prod.yml build backend
```

### 启动生产环境

```bash
# 启动生产服务
docker-compose -f docker-compose.prod.yml up -d

# 查看生产服务状态
docker-compose -f docker-compose.prod.yml ps

# 查看生产日志
docker-compose -f docker-compose.prod.yml logs -f
```

### 更新生产服务

```bash
# 拉取最新代码
git pull origin main

# 重新构建并启动
docker-compose -f docker-compose.prod.yml up -d --build

# 运行数据库迁移
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### 健康检查

```bash
# 检查后端健康状态
curl http://localhost:8000/api/v1/health

# 检查 API 文档
curl http://localhost:8000/docs

# 检查前端
curl http://localhost:5173
```

---

## 故障排查

### 查看容器日志

```bash
# 查看所有容器日志
docker-compose logs

# 查看特定容器的详细日志
docker-compose logs -f --tail=200 backend

# 查看容器启动失败原因
docker-compose logs backend | grep -i error
```

### 检查容器状态

```bash
# 查看容器运行状态
docker-compose ps

# 查看容器详细信息
docker inspect fastapi-backend-dev

# 查看容器资源使用
docker stats fastapi-backend-dev
```

### 网络诊断

```bash
# 查看 Docker 网络
docker network ls

# 检查网络详情
docker network inspect fastapi-vue3-starter-kit_app-network

# 测试容器间连接（从后端 ping 数据库）
docker-compose exec backend ping db
```

### 端口检查

```bash
# 查看端口占用（Windows）
netstat -ano | findstr :8000
netstat -ano | findstr :5173
netstat -ano | findstr :5432

# 查看端口占用（Linux/Mac）
lsof -i :8000
lsof -i :5173
lsof -i :5432
```

### 重置环境

```bash
# 完全重置开发环境
docker-compose down -v
docker-compose up -d --build

# 清理并重建
docker-compose down
docker system prune -f
docker-compose up -d --build
```

### 数据库连接问题

```bash
# 检查数据库是否运行
docker-compose ps db

# 查看数据库日志
docker-compose logs db

# 测试数据库连接
docker-compose exec backend python -c "from app.core.database import engine; print('Database connected!')"

# 手动连接数据库测试
docker-compose exec db psql -U postgres -d fastapi_db -c "SELECT 1;"
```

### Python 依赖问题

```bash
# 进入容器重新安装依赖
docker-compose exec backend pip install -r requirements.txt --no-cache-dir

# 清理 Python 缓存
docker-compose exec backend find . -type d -name __pycache__ -exec rm -rf {} +
```

### 前端构建问题

```bash
# 清理 node_modules 重新安装
docker-compose exec frontend rm -rf node_modules
docker-compose exec frontend npm install

# 清理构建缓存
docker-compose exec frontend npm run clean
docker-compose exec frontend npm run build
```

---

## 性能监控

### 监控资源使用

```bash
# 实时监控所有容器资源
docker stats

# 监控特定容器
docker stats fastapi-backend-dev

# 查看容器进程
docker-compose top
```

### 日志分析

```bash
# 统计请求数量
docker-compose logs backend | grep "Request completed" | wc -l

# 查看慢请求（处理时间 > 1s）
docker-compose logs backend | grep "process_time" | grep -E "[1-9]\.[0-9]{3}s"

# 查看错误日志
docker-compose logs backend | grep -i error
```

---

## 快速参考

### 每日开发工作流

```bash
# 1. 启动开发环境
docker-compose up -d

# 2. 查看日志确认服务启动
docker-compose logs -f backend

# 3. 进行开发...

# 4. 运行测试
docker-compose exec backend pytest tests/ -v

# 5. 代码格式化
docker-compose exec backend black app/ tests/

# 6. 停止服务
docker-compose stop
```

### 版本更新工作流

```bash
# 1. 拉取最新代码
git pull

# 2. 重新构建镜像
docker-compose up -d --build

# 3. 运行数据库迁移
docker-compose exec backend alembic upgrade head

# 4. 重启服务
docker-compose restart
```

---

## 环境变量

查看和编辑环境变量：

```bash
# 编辑环境变量文件
notepad .env  # Windows
nano .env     # Linux/Mac

# 查看当前环境变量
docker-compose config

# 验证环境变量
docker-compose exec backend printenv | grep DATABASE_URL
```

---

## 有用的别名（可选）

将以下内容添加到你的 shell 配置文件（`.bashrc`, `.zshrc` 等）：

```bash
# Docker Compose 别名
alias dc='docker-compose'
alias dcu='docker-compose up -d'
alias dcd='docker-compose down'
alias dcl='docker-compose logs -f'
alias dcr='docker-compose restart'
alias dcp='docker-compose ps'

# 项目特定别名
alias backend-shell='docker-compose exec backend bash'
alias frontend-shell='docker-compose exec frontend sh'
alias db-shell='docker-compose exec db psql -U postgres -d fastapi_db'
alias backend-logs='docker-compose logs -f backend'
alias frontend-logs='docker-compose logs -f frontend'
```

---

## 更多资源

- **Docker 文档**: https://docs.docker.com/
- **Docker Compose 文档**: https://docs.docker.com/compose/
- **FastAPI 文档**: https://fastapi.tiangolo.com/
- **Vue 3 文档**: https://vuejs.org/
- **PostgreSQL 文档**: https://www.postgresql.org/docs/
- **Redis 文档**: https://redis.io/documentation

---

*最后更新: 2025-11-27*

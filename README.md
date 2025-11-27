# FastAPI + Vue 3 Starter Kit

一个生产就绪的全栈开发框架，采用 Monorepo 架构，整合 FastAPI 后端和 Vue 3 前端，全面 Docker 化。

## 技术栈

### 后端
- **框架**: FastAPI 0.109+
- **语言**: Python 3.11+
- **数据库**: PostgreSQL 15 + SQLAlchemy 2.x (异步)
- **缓存**: Redis 7
- **日志**: Structlog (结构化日志)
- **安全**: JWT 认证
- **容器**: Docker 多阶段构建

### 前端
- **框架**: Vue 3.3+ (Composition API)
- **构建**: Vite 5+
- **语言**: TypeScript 5+
- **路由**: Vue Router 4
- **状态**: Pinia 2
- **UI**: Element Plus 2.5+
- **样式**: Tailwind CSS 3+
- **HTTP**: Axios

## 项目结构

```
fastapi-vue3-starter-kit/
├── backend/          # FastAPI 后端
├── frontend/         # Vue 3 前端
├── nginx/            # Nginx 配置
├── docker-compose.yml
├── docker-compose.prod.yml
└── README.md
```

## 快速开始

### 前置要求
- Docker & Docker Compose
- Python 3.11+ (本地开发，可选)
- Node.js 18+ (本地开发，可选)

### 开发环境

1. **克隆项目**
```bash
git clone <repository-url>
cd fastapi-vue3-starter-kit
```

2. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库密码等信息
```

3. **启动开发环境**
```bash
docker-compose up -d
```

4. **访问服务**
- 前端: http://localhost:5173
- 后端 API 文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/api/v1/health

5. **查看日志**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 生产部署

1. **配置生产环境变量**
```bash
cp .env.example .env
# 设置生产环境的密钥和密码
```

2. **构建并启动**
```bash
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

3. **访问服务**
- 统一入口: http://localhost (通过 Nginx 网关)

## 开发指南

### 后端开发

```bash
cd backend

# 安装依赖
pip install -r requirements-dev.txt

# 运行数据库迁移
alembic upgrade head

# 创建新迁移
alembic revision --autogenerate -m "description"

# 本地运行 (不使用 Docker)
uvicorn app.main:app --reload

# 运行测试
pytest tests/ -v

# 代码格式化
black app/ tests/
isort app/ tests/

# 代码检查
flake8 app/ tests/
mypy app/
```

### 前端开发

```bash
cd frontend

# 安装依赖
npm install

# 本地运行 (不使用 Docker)
npm run dev

# 构建生产版本
npm run build

# 代码检查和格式化
npm run lint
npm run format
```

## 架构设计

### 后端分层架构

- **Controller 层** (`api/`): HTTP 请求处理、参数验证
- **Service 层** (`services/`): 业务逻辑、事务管理
- **Repository 层** (`repositories/`): 数据访问、ORM 查询
- **Model 层** (`models/`): SQLAlchemy ORM 模型
- **Schema 层** (`schemas/`): Pydantic 数据验证

### 核心特性

#### 1. 结构化日志
- JSON 格式输出
- 请求 ID 追踪
- 多级别日志控制
- 文件轮转支持

#### 2. 异常处理
- 统一错误响应格式
- 自定义异常类
- 全局异常处理器
- 详细错误日志

#### 3. 数据库管理
- 异步 SQLAlchemy 2.x
- 连接池优化
- Alembic 迁移
- 泛型 Repository 基类

#### 4. 安全特性
- JWT 令牌认证
- 密码哈希 (bcrypt)
- CORS 配置
- 请求验证

#### 5. Docker 优化
- 多阶段构建
- 镜像体积优化
- 健康检查
- 热重载支持

## API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 环境变量

关键环境变量说明：

```bash
# 应用配置
APP_NAME=FastAPI Starter Kit
DEBUG=false

# 数据库
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/dbname

# Redis
REDIS_URL=redis://redis:6379/0

# 安全
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 日志
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## 代码规范

### 后端
- **Black**: 代码格式化 (行长度: 100)
- **isort**: 导入排序
- **Flake8**: 代码检查
- **MyPy**: 类型检查

### 前端
- **ESLint**: 代码检查
- **Prettier**: 代码格式化
- **TypeScript**: 严格模式

## 测试

### 后端测试
```bash
# 运行所有测试
pytest tests/ -v

# 测试覆盖率
pytest tests/ --cov=app --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html
```

### 前端测试
```bash
# 单元测试 (需配置)
npm run test

# E2E 测试 (需配置)
npm run test:e2e
```

## 故障排查

### 常见问题

**1. 数据库连接失败**
- 检查 `.env` 中的 `DATABASE_URL`
- 确认 PostgreSQL 容器正常运行: `docker-compose ps`

**2. 前端无法访问后端 API**
- 检查 CORS 配置
- 确认 `VITE_API_BASE_URL` 环境变量

**3. Docker 构建失败**
- 清理缓存: `docker-compose down -v`
- 重新构建: `docker-compose build --no-cache`

## 扩展建议

- [ ] CI/CD 流水线 (GitHub Actions / GitLab CI)
- [ ] 容器编排 (Kubernetes)
- [ ] 监控系统 (Prometheus + Grafana)
- [ ] 日志聚合 (ELK Stack)
- [ ] 分布式追踪 (OpenTelemetry)
- [ ] API 网关 (Kong / Traefik)
- [ ] 消息队列 (Celery + Redis)
- [ ] 对象存储 (S3 / MinIO)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

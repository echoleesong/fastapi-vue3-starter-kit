#!/bin/bash

echo "======================================"
echo "FastAPI Vue3 Starter Kit - 开发环境启动"
echo "======================================"
echo ""

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker 未运行，请先启动 Docker"
    exit 1
fi

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "📝 创建 .env 文件..."
    cp .env.example .env
    echo "✅ .env 文件已创建，请检查并修改配置"
    echo ""
fi

# 启动开发环境
echo "🚀 启动开发环境..."
docker-compose up -d

# 等待服务启动
echo ""
echo "⏳ 等待服务启动..."
sleep 5

# 显示服务状态
echo ""
echo "📊 服务状态："
docker-compose ps

echo ""
echo "======================================"
echo "✅ 开发环境启动完成！"
echo "======================================"
echo ""
echo "🌐 访问地址："
echo "   - 前端：http://localhost:5173"
echo "   - 后端 API 文档：http://localhost:8000/docs"
echo "   - 健康检查：http://localhost:8000/api/v1/health"
echo ""
echo "📝 查看日志："
echo "   docker-compose logs -f backend"
echo "   docker-compose logs -f frontend"
echo ""
echo "🛑 停止服务："
echo "   docker-compose down"
echo ""

# ==================== Stage 1: Build Stage ====================
FROM node:18-alpine as build-stage

WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制源代码
COPY . .

# 构建生产版本
RUN npm run build

# ==================== Stage 2: Production Stage (Nginx) ====================
FROM nginx:alpine as production-stage

# 复制自定义 nginx 配置 (如果需要)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# 从 build-stage 复制构建产物
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 暴露端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]

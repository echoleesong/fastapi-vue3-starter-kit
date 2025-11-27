<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <div class="container mx-auto px-4 py-16">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-5xl font-bold text-gray-900 mb-4">
          FastAPI + Vue 3 Starter Kit
        </h1>
        <p class="text-xl text-gray-600 mb-8">
          生产就绪的全栈开发框架 - Monorepo + Docker
        </p>
      </div>

      <!-- Features Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        <el-card class="feature-card" shadow="hover">
          <template #header>
            <div class="flex items-center">
              <span class="text-2xl mr-2">🚀</span>
              <span class="font-semibold">快速开发</span>
            </div>
          </template>
          <p class="text-gray-600">
            开箱即用的全栈框架，热重载支持，快速迭代开发
          </p>
        </el-card>

        <el-card class="feature-card" shadow="hover">
          <template #header>
            <div class="flex items-center">
              <span class="text-2xl mr-2">🏗️</span>
              <span class="font-semibold">分层架构</span>
            </div>
          </template>
          <p class="text-gray-600">
            Controller/Service/Repository 三层架构，清晰的职责划分
          </p>
        </el-card>

        <el-card class="feature-card" shadow="hover">
          <template #header>
            <div class="flex items-center">
              <span class="text-2xl mr-2">🐳</span>
              <span class="font-semibold">Docker 化</span>
            </div>
          </template>
          <p class="text-gray-600">
            多阶段构建，开发/生产环境完全容器化
          </p>
        </el-card>

        <el-card class="feature-card" shadow="hover">
          <template #header>
            <div class="flex items-center">
              <span class="text-2xl mr-2">📝</span>
              <span class="font-semibold">结构化日志</span>
            </div>
          </template>
          <p class="text-gray-600">
            JSON 格式日志，请求追踪，完整的可观测性
          </p>
        </el-card>

        <el-card class="feature-card" shadow="hover">
          <template #header>
            <div class="flex items-center">
              <span class="text-2xl mr-2">🔒</span>
              <span class="font-semibold">安全认证</span>
            </div>
          </template>
          <p class="text-gray-600">
            JWT 令牌认证，密码哈希，完整的安全机制
          </p>
        </el-card>

        <el-card class="feature-card" shadow="hover">
          <template #header>
            <div class="flex items-center">
              <span class="text-2xl mr-2">⚡</span>
              <span class="font-semibold">高性能</span>
            </div>
          </template>
          <p class="text-gray-600">
            异步 FastAPI + Vue 3 + PostgreSQL，极致性能
          </p>
        </el-card>
      </div>

      <!-- Actions -->
      <div class="text-center space-x-4">
        <el-button type="primary" size="large" @click="goToUsers">
          查看用户管理
        </el-button>
        <el-button size="large" @click="goToApiDocs">
          API 文档
        </el-button>
      </div>

      <!-- Tech Stack -->
      <div class="mt-16 text-center">
        <h2 class="text-2xl font-semibold text-gray-800 mb-6">技术栈</h2>
        <div class="flex flex-wrap justify-center gap-3">
          <el-tag size="large">FastAPI 0.109</el-tag>
          <el-tag size="large" type="success">Vue 3.3</el-tag>
          <el-tag size="large" type="info">TypeScript 5</el-tag>
          <el-tag size="large" type="warning">Pinia 2</el-tag>
          <el-tag size="large" type="danger">Element Plus 2.5</el-tag>
          <el-tag size="large">Tailwind CSS 3</el-tag>
          <el-tag size="large" type="success">PostgreSQL 15</el-tag>
          <el-tag size="large" type="info">Docker</el-tag>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goToUsers = () => {
  router.push('/users')
}

const goToApiDocs = () => {
  window.open('http://localhost:8000/docs', '_blank')
}
</script>

<style scoped>
.feature-card {
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-4px);
}
</style>

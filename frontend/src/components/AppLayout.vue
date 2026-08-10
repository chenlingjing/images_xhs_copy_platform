<template>
  <div class="min-h-screen flex flex-col bg-xhs-bg">
    <!-- Header -->
    <header class="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-xhs-red flex items-center justify-center text-white font-bold text-lg shadow-lg shadow-red-200">
            红
          </div>
          <div class="flex flex-col">
            <span class="font-bold text-lg leading-tight text-gray-900">小红书文案生成平台</span>
            <span class="text-xs text-gray-500 hidden sm:block">AI 图片转种草文案工作台</span>
          </div>
        </div>

        <nav class="flex items-center gap-1 sm:gap-2">
          <RouterLink
            to="/workspace"
            class="px-4 py-2 rounded-xl text-sm font-medium transition-colors"
            :class="$route.path === '/workspace' || $route.path === '/' ? 'text-xhs-red bg-red-50' : 'text-gray-600 hover:bg-gray-50'"
          >
            工作台
          </RouterLink>
        </nav>
      </div>
    </header>

    <!-- Main content -->
    <main class="flex-1">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-100 py-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-sm text-gray-500">
          © 2026 小红书文案生成平台 · 仅供学习交流
        </p>
        <div class="flex items-center gap-6 text-sm text-gray-500">
          <a href="#" class="hover:text-xhs-red transition-colors">使用说明</a>
          <a href="#" class="hover:text-xhs-red transition-colors">GitHub</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

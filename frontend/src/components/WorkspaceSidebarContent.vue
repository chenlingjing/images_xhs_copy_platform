<template>
  <div class="flex flex-col h-full">
    <div class="hidden lg:flex h-16 items-center px-6 border-b border-gray-100">
      <RouterLink
        to="/"
        class="flex items-center gap-3"
      >
        <div class="w-8 h-8 rounded-lg bg-xhs-red flex items-center justify-center text-white font-bold text-sm">
          红
        </div>
        <span class="font-bold text-gray-900">工作台</span>
      </RouterLink>
    </div>

    <nav class="flex-1 p-4 space-y-1">
      <RouterLink
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors"
        :class="isActive(item.path) ? 'bg-red-50 text-xhs-red' : 'text-gray-600 hover:bg-gray-50'"
      >
        <svg
          class="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          v-html="item.icon"
        />
        {{ item.label }}
      </RouterLink>
    </nav>

    <div class="p-4 border-t border-gray-100">
      <div class="flex items-center gap-3 px-4 py-3">
        <img
          v-if="auth.currentUser?.avatar"
          :src="auth.currentUser.avatar"
          alt="avatar"
          class="w-9 h-9 rounded-full bg-gray-100"
        >
        <div
          v-else
          class="w-9 h-9 rounded-full bg-gray-100 flex items-center justify-center text-sm font-bold text-gray-500"
        >
          {{ auth.currentUser?.username?.[0]?.toUpperCase() ?? 'U' }}
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 truncate">
            {{ auth.currentUser?.username }}
          </p>
          <p class="text-xs text-gray-500 truncate">
            {{ auth.isAdmin ? '管理员' : '普通用户' }}
          </p>
        </div>
      </div>
      <button
        type="button"
        class="w-full mt-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-xl transition-colors text-left flex items-center gap-2"
        @click="emit('logout')"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
        退出登录
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const emit = defineEmits<{
  logout: []
}>()

const route = useRoute()
const auth = useAuthStore()

const menuItems = [
  {
    path: '/workspace/generate',
    label: '文案生成',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z" />'
  },
  {
    path: '/workspace/history',
    label: '历史记录',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />'
  }
]

function isActive(path: string) {
  return route.path === path
}
</script>

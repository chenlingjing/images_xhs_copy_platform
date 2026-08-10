<template>
  <div class="flex flex-col h-full">
    <div class="hidden lg:flex h-16 items-center px-6 border-b border-gray-100">
      <div
        class="flex items-center gap-3"
      >
        <div class="w-8 h-8 rounded-lg bg-xhs-red flex items-center justify-center text-white font-bold text-sm">
          红
        </div>
        <span class="font-bold text-gray-900">工作台</span>
      </div>
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
      <RouterLink
        to="/workspace/profile"
        class="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-gray-50 transition-colors"
      >
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
      </RouterLink>

      <RouterLink
        to="/"
        class="w-full mt-2 px-4 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded-xl transition-colors text-left flex items-center gap-2"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
        返回首页
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const auth = useAuthStore()

const menuItems = computed(() => {
  const items = [
    {
      path: '/workspace/generate',
      label: '文案生成',
      icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z" />'
    },
    {
      path: '/workspace/history',
      label: '历史记录',
      icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />'
    },
    {
      path: '/workspace/profile',
      label: '个人中心',
      icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />'
    }
  ]

  if (auth.isAdmin) {
    items.push({
      path: '/admin',
      label: '后台管理',
      icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />'
    })
  }

  return items
})

function isActive(path: string) {
  if (path === '/admin') return route.path.startsWith('/admin')
  return route.path === path
}
</script>

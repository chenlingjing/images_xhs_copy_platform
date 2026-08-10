<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-white border-r border-gray-200 flex-col hidden lg:flex">
      <div class="h-16 flex items-center px-6 border-b border-gray-100">
        <RouterLink
          to="/"
          class="flex items-center gap-3"
        >
          <div class="w-8 h-8 rounded-lg bg-xhs-red flex items-center justify-center text-white font-bold text-sm">
            红
          </div>
          <span class="font-bold text-gray-900">管理后台</span>
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
          <div class="w-9 h-9 rounded-full bg-gray-100 flex items-center justify-center text-gray-600 font-bold text-sm">
            {{ auth.currentUser?.username?.[0]?.toUpperCase() ?? 'A' }}
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
          class="w-full mt-2 px-4 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded-xl transition-colors text-left"
          @click="backToWorkspace"
        >
          返回工作台
        </button>
      </div>
    </aside>

    <!-- Mobile header -->
    <div class="lg:hidden fixed top-0 left-0 right-0 z-50 bg-white border-b border-gray-200 h-14 flex items-center justify-between px-4">
      <span class="font-bold text-gray-900">管理后台</span>
      <button
        type="button"
        class="p-2 rounded-lg hover:bg-gray-100"
        @click="mobileMenuOpen = !mobileMenuOpen"
      >
        <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
    </div>

    <!-- Mobile menu -->
    <div
      v-if="mobileMenuOpen"
      class="lg:hidden fixed inset-0 z-40 bg-black/20"
      @click="mobileMenuOpen = false"
    >
      <div
        class="absolute top-14 left-0 right-0 bg-white border-b border-gray-200 p-4 space-y-1 shadow-lg"
        @click.stop
      >
        <RouterLink
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors"
          :class="isActive(item.path) ? 'bg-red-50 text-xhs-red' : 'text-gray-600 hover:bg-gray-50'"
          @click="mobileMenuOpen = false"
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
      </div>
    </div>

    <!-- Main content -->
    <div class="flex-1 flex flex-col min-w-0">
      <header class="hidden lg:flex h-16 bg-white border-b border-gray-200 items-center justify-between px-8">
        <h1 class="text-lg font-semibold text-gray-900">{{ pageTitle }}</h1>
        <div class="flex items-center gap-3">
          <span class="text-xs px-2.5 py-1 rounded-full bg-red-50 text-xhs-red font-medium">管理员模式</span>
        </div>
      </header>
      <main class="flex-1 p-4 lg:p-8 pt-20 lg:pt-8 overflow-auto">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const mobileMenuOpen = ref(false)

const menuItems = [
  {
    path: '/admin',
    label: '用量概览',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />'
  },
  {
    path: '/admin/users',
    label: '用户管理',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />'
  },
  {
    path: '/admin/generations',
    label: '生成记录',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />'
  }
]

const pageTitle = computed(() => {
  return menuItems.find(item => item.path === route.path)?.label ?? '管理后台'
})

function isActive(path: string) {
  return route.path === path || (path !== '/admin' && route.path.startsWith(path))
}

function backToWorkspace() {
  router.push('/workspace')
}
</script>

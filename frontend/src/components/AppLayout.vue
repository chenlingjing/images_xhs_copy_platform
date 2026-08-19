<template>
  <div class="min-h-screen flex flex-col bg-xhs-bg">
    <!-- Header -->
    <header class="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <!-- Logo -->
        <RouterLink
          to="/"
          class="flex items-center gap-2.5 flex-shrink-0"
        >
          <div class="w-8 h-8 rounded-lg bg-xhs-red flex items-center justify-center text-white font-bold text-base shadow-md shadow-red-200">
            红
          </div>
          <span class="font-bold text-lg text-gray-900">小红书文案生成</span>
        </RouterLink>

        <!-- Desktop nav -->
        <nav class="hidden md:flex items-center gap-1">
          <RouterLink
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            :class="isActive(item.path) ? 'text-xhs-red' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'"
          >
            {{ item.label }}
          </RouterLink>
        </nav>

        <!-- Right actions -->
        <div class="flex items-center gap-2 sm:gap-3">
          <template v-if="!auth.isLoggedIn">
            <RouterLink
              to="/login"
              class="hidden sm:inline-flex px-4 py-2 rounded-lg text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 transition-colors"
            >
              登录
            </RouterLink>
            <RouterLink
              to="/register"
              class="btn-primary text-sm px-4 py-2"
            >
              免费开始
            </RouterLink>
          </template>

          <template v-else>
            <RouterLink
              to="/workspace"
              class="btn-primary text-sm px-4 py-2"
            >
              进入工作台
            </RouterLink>

            <!-- User dropdown -->
            <div
              ref="userDropdownRef"
              class="relative hidden sm:block"
            >
              <button
                type="button"
                class="flex items-center gap-2 pl-1 pr-2 py-1 rounded-full border border-gray-200 bg-white hover:border-gray-300 transition-colors"
                @click="userMenuOpen = !userMenuOpen"
              >
                <img
                  v-if="auth.currentUser?.avatar"
                  :src="auth.currentUser.avatar"
                  alt="avatar"
                  class="w-7 h-7 rounded-full bg-gray-100"
                >
                <div
                  v-else
                  class="w-7 h-7 rounded-full bg-red-50 flex items-center justify-center text-xs font-bold text-xhs-red"
                >
                  {{ auth.currentUser?.username?.[0]?.toUpperCase() ?? 'U' }}
                </div>
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <div
                v-if="userMenuOpen"
                class="absolute right-0 mt-2 w-56 bg-white rounded-2xl shadow-xl border border-gray-100 py-2"
              >
                <div class="px-4 py-3 border-b border-gray-100">
                  <p class="text-sm font-semibold text-gray-900 truncate">
                    {{ auth.currentUser?.username }}
                  </p>
                  <p class="text-xs text-gray-500 truncate">
                    {{ auth.currentUser?.email }}
                  </p>
                  <p class="text-xs text-xhs-red mt-1">
                    {{ auth.isAdmin ? '管理员' : '普通用户' }}
                  </p>
                </div>
                <RouterLink
                  v-if="auth.isAdmin"
                  to="/admin"
                  class="flex items-center gap-2 px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                  @click="userMenuOpen = false"
                >
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                  </svg>
                  后台管理
                </RouterLink>
                <button
                  type="button"
                  class="w-full flex items-center gap-2 px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 transition-colors"
                  @click="logoutMenu"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  退出登录
                </button>
              </div>
            </div>
          </template>

          <!-- Mobile menu button -->
          <button
            type="button"
            class="md:hidden p-2 rounded-lg hover:bg-gray-100"
            aria-label="打开菜单"
            @click="mobileMenuOpen = true"
          >
            <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- Mobile menu drawer -->
    <Transition
      enter-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="mobileMenuOpen"
        class="fixed inset-0 z-50 md:hidden"
      >
        <div
          class="absolute inset-0 bg-black/40"
          @click="mobileMenuOpen = false"
        />
        <div class="absolute right-0 top-0 bottom-0 w-64 bg-white shadow-2xl flex flex-col">
          <div class="h-16 flex items-center justify-between px-4 border-b border-gray-100">
            <span class="font-bold text-gray-900">菜单</span>
            <button
              type="button"
              class="p-2 rounded-lg hover:bg-gray-100"
              aria-label="关闭菜单"
              @click="mobileMenuOpen = false"
            >
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Mobile user info -->
          <div
            v-if="auth.isLoggedIn"
            class="px-4 py-4 border-b border-gray-100"
          >
            <div class="flex items-center gap-3">
              <img
                v-if="auth.currentUser?.avatar"
                :src="auth.currentUser.avatar"
                alt="avatar"
                class="w-10 h-10 rounded-full bg-gray-100"
              >
              <div
                v-else
                class="w-10 h-10 rounded-full bg-red-50 flex items-center justify-center text-sm font-bold text-xhs-red"
              >
                {{ auth.currentUser?.username?.[0]?.toUpperCase() ?? 'U' }}
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-semibold text-gray-900 truncate">
                  {{ auth.currentUser?.username }}
                </p>
                <p class="text-xs text-gray-500 truncate">
                  {{ auth.currentUser?.email }}
                </p>
                <p class="text-xs text-xhs-red mt-0.5">
                  {{ auth.isAdmin ? '管理员' : '普通用户' }}
                </p>
              </div>
            </div>
          </div>

          <nav class="p-4 space-y-1 flex-1">
            <RouterLink
              v-for="item in navItems"
              :key="item.path"
              :to="item.path"
              class="block px-4 py-3 rounded-xl text-sm font-medium transition-colors"
              :class="isActive(item.path) ? 'bg-red-50 text-xhs-red' : 'text-gray-600 hover:bg-gray-50'"
              @click="mobileMenuOpen = false"
            >
              {{ item.label }}
            </RouterLink>
          </nav>
          <div class="p-4 border-t border-gray-100 space-y-2">
            <template v-if="!auth.isLoggedIn">
              <RouterLink
                to="/login"
                class="block w-full text-center px-4 py-2.5 rounded-xl text-sm font-medium text-gray-600 hover:bg-gray-50"
                @click="mobileMenuOpen = false"
              >
                登录
              </RouterLink>
              <RouterLink
                to="/register"
                class="block w-full text-center btn-primary text-sm px-4 py-2.5"
                @click="mobileMenuOpen = false"
              >
                免费开始
              </RouterLink>
            </template>
            <template v-else>
              <RouterLink
                to="/workspace"
                class="block w-full text-center btn-primary text-sm px-4 py-2.5"
                @click="mobileMenuOpen = false"
              >
                进入工作台
              </RouterLink>
              <button
                type="button"
                class="block w-full text-center px-4 py-2.5 rounded-xl text-sm font-medium text-red-600 hover:bg-red-50"
                @click="logoutMobile"
              >
                退出登录
              </button>
            </template>
          </div>
        </div>
      </div>
    </Transition>

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
          <a href="https://github.com/chenlingjing/images_xhs_copy_platform" class="hover:text-xhs-red transition-colors">GitHub</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useHistoryStore } from '@/stores/history'

const auth = useAuthStore()
const historyStore = useHistoryStore()
const router = useRouter()
const route = useRoute()
const mobileMenuOpen = ref(false)
const userMenuOpen = ref(false)
const userDropdownRef = ref<HTMLElement | null>(null)

function closeUserMenuOnClickOutside(event: MouseEvent) {
  if (userMenuOpen.value && userDropdownRef.value && !userDropdownRef.value.contains(event.target as Node)) {
    userMenuOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', closeUserMenuOnClickOutside))
onUnmounted(() => document.removeEventListener('click', closeUserMenuOnClickOutside))

const navItems = [
  { path: '/', label: '首页' },
  { path: '/#features', label: '功能' },
  { path: '/#example', label: '效果示例' },
  { path: '/#faq', label: '常见问题' }
]

function isActive(path: string) {
  if (path === '/') return route.path === '/' && !route.hash
  const hash = path.split('#')[1]
  return route.hash === `#${hash}`
}

function logout() {
  auth.logout()
  historyStore.clearHistory()
  router.push('/')
}

function logoutMenu() {
  userMenuOpen.value = false
  logout()
}

function logoutMobile() {
  mobileMenuOpen.value = false
  logout()
}
</script>

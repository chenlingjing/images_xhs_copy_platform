<template>
  <AdminLayout>
    <div class="bg-white rounded-2xl border border-gray-100 shadow-card overflow-hidden">
      <div class="p-6 border-b border-gray-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 class="text-lg font-bold text-gray-900">用户列表</h2>
          <p class="text-sm text-gray-500 mt-1">查看平台注册用户与管理员信息</p>
        </div>
        <div class="relative">
          <input
            v-model="search"
            type="text"
            placeholder="搜索用户名或邮箱"
            class="input !pl-12"
          >
          <svg class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      <LoadingState
        v-if="loading"
        title="加载用户数据中"
      />

      <div
        v-else
        class="overflow-x-auto"
      >
        <table class="w-full text-left text-sm">
          <thead class="bg-gray-50 text-gray-500">
            <tr>
              <th class="px-6 py-4 font-medium">用户</th>
              <th class="px-6 py-4 font-medium">邮箱</th>
              <th class="px-6 py-4 font-medium">角色</th>
              <th class="px-6 py-4 font-medium">注册时间</th>
              <th class="px-6 py-4 font-medium">最近活跃</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr
              v-for="user in filteredUsers"
              :key="user.id"
              class="hover:bg-gray-50/50 transition-colors"
            >
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <img
                    v-if="user.avatar"
                    :src="user.avatar"
                    alt="avatar"
                    class="w-9 h-9 rounded-full bg-gray-100"
                  >
                  <div
                    v-else
                    class="w-9 h-9 rounded-full bg-gray-100 flex items-center justify-center text-xs font-bold text-gray-500"
                  >
                    {{ user.username[0].toUpperCase() }}
                  </div>
                  <span class="font-medium text-gray-900">{{ user.username }}</span>
                </div>
              </td>
              <td class="px-6 py-4 text-gray-600">{{ user.email }}</td>
              <td class="px-6 py-4">
                <span
                  class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                  :class="user.role === 'admin' ? 'bg-red-50 text-xhs-red' : 'bg-gray-100 text-gray-600'"
                >
                  {{ user.role === 'admin' ? '管理员' : '普通用户' }}
                </span>
              </td>
              <td class="px-6 py-4 text-gray-500">{{ formatDate(user.createdAt) }}</td>
              <td class="px-6 py-4 text-gray-500">{{ formatTime(user.lastActiveAt) }}</td>
            </tr>
          </tbody>
        </table>

        <div
          v-if="filteredUsers.length === 0"
          class="py-12 text-center text-sm text-gray-500"
        >
          未找到匹配的用户
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import LoadingState from '@/components/LoadingState.vue'
import { getUsers } from '@/services/adminApi'
import type { User } from '@/types'

const users = ref<User[]>([])
const loading = ref(false)
const search = ref('')

const filteredUsers = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return users.value
  return users.value.filter(u =>
    u.username.toLowerCase().includes(q) ||
    u.email.toLowerCase().includes(q)
  )
})

async function load() {
  loading.value = true
  try {
    users.value = await getUsers()
  } finally {
    loading.value = false
  }
}

function formatDate(isoString: string) {
  return new Date(isoString).toLocaleDateString('zh-CN')
}

function formatTime(isoString: string) {
  const date = new Date(isoString)
  return date.toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(load)
</script>

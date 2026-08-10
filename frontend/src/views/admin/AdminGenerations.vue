<template>
  <AdminLayout>
    <div class="space-y-5">
      <!-- Filters -->
      <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-card flex flex-col sm:flex-row gap-4">
        <div class="relative flex-1">
          <input
            v-model="search"
            type="text"
            placeholder="搜索标题或用户名"
            class="input !pl-12"
          >
          <svg class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <select
          v-model="statusFilter"
          class="input sm:w-40"
        >
          <option value="all">全部状态</option>
          <option value="success">成功</option>
          <option value="failed">失败</option>
        </select>
      </div>

      <!-- Records table -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-card overflow-hidden">
        <LoadingState
          v-if="loading"
          title="加载生成记录中"
        />

        <div
          v-else
          class="overflow-x-auto"
        >
          <table class="w-full text-left text-sm">
            <thead class="bg-gray-50 text-gray-500">
              <tr>
                <th class="px-6 py-4 font-medium">图片</th>
                <th class="px-6 py-4 font-medium">标题</th>
                <th class="px-6 py-4 font-medium">用户</th>
                <th class="px-6 py-4 font-medium">状态</th>
                <th class="px-6 py-4 font-medium">生成时间</th>
                <th class="px-6 py-4 font-medium">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr
                v-for="record in filteredRecords"
                :key="record.id"
                class="hover:bg-gray-50/50 transition-colors"
              >
                <td class="px-6 py-4">
                  <div class="w-14 h-14 rounded-xl bg-gray-100 overflow-hidden">
                    <img
                      :src="record.imageUrl"
                      alt="生成图片"
                      class="w-full h-full object-cover"
                    >
                  </div>
                </td>
                <td class="px-6 py-4">
                  <p class="font-medium text-gray-900 max-w-xs truncate">
                    {{ record.result?.title || '生成失败' }}
                  </p>
                  <p
                    v-if="record.errorMessage"
                    class="text-xs text-red-500 mt-1 max-w-xs truncate"
                  >
                    {{ record.errorMessage }}
                  </p>
                </td>
                <td class="px-6 py-4">
                  <div class="flex items-center gap-2">
                    <img
                      v-if="record.user.avatar"
                      :src="record.user.avatar"
                      alt="avatar"
                      class="w-6 h-6 rounded-full bg-gray-100"
                    >
                    <span class="text-gray-600">{{ record.user.username }}</span>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <span
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                    :class="record.status === 'success' ? 'bg-green-50 text-green-600' : 'bg-red-50 text-xhs-red'"
                  >
                    {{ record.status === 'success' ? '成功' : '失败' }}
                  </span>
                </td>
                <td class="px-6 py-4 text-gray-500">
                  {{ formatTime(record.createdAt) }}
                </td>
                <td class="px-6 py-4">
                  <button
                    type="button"
                    class="text-sm text-xhs-red hover:text-red-700 font-medium"
                    @click="remove(record.id)"
                  >
                    删除
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <div
            v-if="filteredRecords.length === 0"
            class="py-12 text-center text-sm text-gray-500"
          >
            未找到匹配的记录
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import LoadingState from '@/components/LoadingState.vue'
import { getGenerations, deleteGeneration } from '@/services/adminApi'
import type { AdminGenerationRecord } from '@/types'

const records = ref<AdminGenerationRecord[]>([])
const loading = ref(false)
const search = ref('')
const statusFilter = ref<'all' | 'success' | 'failed'>('all')

const filteredRecords = computed(() => {
  return records.value.filter(r => {
    const q = search.value.trim().toLowerCase()
    const matchesSearch = !q ||
      (r.result?.title ?? '').toLowerCase().includes(q) ||
      r.user.username.toLowerCase().includes(q)
    const matchesStatus = statusFilter.value === 'all' || r.status === statusFilter.value
    return matchesSearch && matchesStatus
  })
})

async function load() {
  loading.value = true
  try {
    records.value = await getGenerations()
  } finally {
    loading.value = false
  }
}

async function remove(id: string) {
  if (!confirm('确定要删除这条生成记录吗？')) return
  await deleteGeneration(id)
  records.value = records.value.filter(r => r.id !== id)
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

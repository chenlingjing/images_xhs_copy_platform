<template>
  <div class="max-w-6xl mx-auto">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">历史记录</h1>
      <p class="text-gray-500">查看并回溯你过往生成的所有小红书文案</p>
    </div>

    <!-- Filters -->
    <div class="card p-4 sm:p-5 mb-6 flex flex-col sm:flex-row gap-4">
      <div class="relative flex-1">
        <input
          v-model="search"
          type="text"
          placeholder="搜索标题或关键词"
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

    <!-- Empty state -->
    <EmptyState
      v-if="historyStore.isEmpty"
      title="暂无历史记录"
      description="在工作台生成文案后，所有记录都会保存在这里，方便随时回溯。"
    />

    <EmptyState
      v-else-if="filteredRecords.length === 0"
      title="未找到匹配记录"
      description="尝试更换搜索关键词或筛选条件。"
    />

    <!-- Records list -->
    <div
      v-else
      class="space-y-4"
    >
      <div
        v-for="record in filteredRecords"
        :key="record.id"
        class="card p-4 sm:p-5 hover:shadow-float transition-shadow"
      >
        <div class="flex flex-row gap-4 sm:gap-5">
          <!-- Image -->
          <div class="w-24 h-24 sm:w-32 sm:h-32 lg:w-48 lg:h-auto flex-shrink-0">
            <div class="w-full h-full rounded-xl bg-gray-100 overflow-hidden">
              <img
                :src="record.imageUrl"
                alt="历史图片"
                class="w-full h-full object-cover"
              >
            </div>
          </div>

          <!-- Content -->
          <div class="flex-1 min-w-0">
            <div class="flex flex-wrap items-center gap-2 mb-2">
              <span
                class="px-2.5 py-1 rounded-full text-xs font-medium"
                :class="record.status === 'success' ? 'bg-green-50 text-green-600' : 'bg-red-50 text-xhs-red'"
              >
                {{ record.status === 'success' ? '生成成功' : '生成失败' }}
              </span>
              <span class="text-xs text-gray-400">{{ formatTime(record.createdAt) }}</span>
            </div>

            <h3 class="text-lg font-bold text-gray-900 mb-2 line-clamp-2">
              {{ record.result?.title || '生成失败' }}
            </h3>

            <p
              v-if="record.errorMessage"
              class="text-sm text-red-500 mb-3"
            >
              {{ record.errorMessage }}
            </p>

            <p
              v-else-if="record.result"
              class="text-sm text-gray-600 line-clamp-3 mb-3 leading-relaxed"
            >
              {{ record.result.content }}
            </p>

            <div
              v-if="record.result?.tags"
              class="flex flex-wrap gap-2 mb-4"
            >
              <span
                v-for="tag in record.result.tags"
                :key="tag"
                class="px-2.5 py-1 rounded-full bg-blue-50 text-blue-600 text-xs font-medium"
              >
                {{ tag }}
              </span>
            </div>

            <!-- Params summary -->
            <div class="flex flex-wrap gap-2 mb-4">
              <span
                v-if="record.params.productName"
                class="text-xs px-2 py-1 rounded-lg bg-gray-100 text-gray-600"
              >
                产品：{{ record.params.productName }}
              </span>
              <span
                v-if="record.params.targetAudience"
                class="text-xs px-2 py-1 rounded-lg bg-gray-100 text-gray-600"
              >
                人群：{{ record.params.targetAudience }}
              </span>
              <span
                v-if="record.params.toneStyle"
                class="text-xs px-2 py-1 rounded-lg bg-gray-100 text-gray-600"
              >
                风格：{{ record.params.toneStyle }}
              </span>
            </div>

            <!-- Actions -->
            <div class="flex flex-wrap gap-3">
              <button
                type="button"
                class="btn-primary text-sm py-2"
                @click="restore(record)"
              >
                <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                回溯到工作台
              </button>
              <button
                v-if="record.result"
                type="button"
                class="btn-secondary text-sm py-2"
                @click="copyFull(record)"
              >
                <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                </svg>
                复制全文
              </button>
              <button
                type="button"
                class="btn-secondary text-sm py-2 text-red-600 hover:text-red-700 hover:bg-red-50 border-red-100"
                @click="remove(record.id)"
              >
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useHistoryStore } from '@/stores/history'
import { useGenerationStore } from '@/stores/generation'
import { copyText } from '@/utils/clipboard'
import EmptyState from '@/components/EmptyState.vue'
import type { GenerationRecord } from '@/types'

const router = useRouter()
const historyStore = useHistoryStore()
const generationStore = useGenerationStore()

const search = ref('')
const statusFilter = ref<'all' | 'success' | 'failed'>('all')

const filteredRecords = computed(() => {
  return historyStore.sortedRecords.filter(r => {
    const q = search.value.trim().toLowerCase()
    const matchesSearch = !q ||
      (r.result?.title ?? '').toLowerCase().includes(q) ||
      (r.result?.content ?? '').toLowerCase().includes(q) ||
      r.params.productName?.toLowerCase().includes(q)
    const matchesStatus = statusFilter.value === 'all' || r.status === statusFilter.value
    return matchesSearch && matchesStatus
  })
})

function restore(record: GenerationRecord) {
  generationStore.restoreRecord(record)
  router.push('/workspace/generate')
}

async function copyFull(record: GenerationRecord) {
  if (!record.result) return
  const { title, content, tags } = record.result
  const fullText = `${title}\n\n${content}\n\n${tags.join(' ')}`
  try {
    await copyText(fullText)
    alert('全文已复制到剪贴板')
  } catch {
    alert('复制失败，请手动复制')
  }
}

async function remove(id: string) {
  if (!confirm('确定要删除这条历史记录吗？')) return
  try {
    await historyStore.deleteRecord(id)
  } catch (error) {
    alert(error instanceof Error ? error.message : '删除失败')
  }
}

function formatTime(isoString: string) {
  const date = new Date(isoString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

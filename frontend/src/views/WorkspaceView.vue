<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Page header -->
    <div class="mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">文案生成工作台</h1>
      <p class="text-gray-500">上传图片，AI 自动识别内容并生成小红书风格种草文案</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      <!-- Left column: input & params -->
      <div class="lg:col-span-5 space-y-6">
        <!-- Image input card -->
        <section class="card p-5 sm:p-6">
          <div class="flex items-center gap-2 mb-5">
            <div class="w-8 h-8 rounded-lg bg-red-50 flex items-center justify-center">
              <svg class="w-5 h-5 text-xhs-red" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h2 class="text-lg font-semibold text-gray-900">图片输入</h2>
          </div>
          <ImageUploader />
        </section>

        <!-- Params card -->
        <section class="card p-5 sm:p-6">
          <div class="flex items-center gap-2 mb-5">
            <div class="w-8 h-8 rounded-lg bg-red-50 flex items-center justify-center">
              <svg class="w-5 h-5 text-xhs-red" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
              </svg>
            </div>
            <h2 class="text-lg font-semibold text-gray-900">生成参数</h2>
          </div>
          <ParamForm
            :disabled="!store.currentImageUrl"
            :is-generating="store.isGenerating"
            @submit="onGenerate"
          />
        </section>
      </div>

      <!-- Right column: result -->
      <div class="lg:col-span-7">
        <section class="card p-5 sm:p-6 min-h-[520px]">
          <div class="flex items-center justify-between mb-5">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-lg bg-red-50 flex items-center justify-center">
                <svg class="w-5 h-5 text-xhs-red" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h2 class="text-lg font-semibold text-gray-900">生成结果</h2>
            </div>
            <span
              v-if="store.status !== 'idle'"
              class="text-xs font-medium px-2.5 py-1 rounded-full"
              :class="statusBadgeClass"
            >
              {{ statusText }}
            </span>
          </div>

          <!-- Idle empty state -->
          <EmptyState
            v-if="store.status === 'idle'"
            title="等待生成"
            description="在左侧上传图片并填写生成参数，点击生成后即可在这里查看小红书风格文案。"
          />

          <!-- Uploading / Generating -->
          <LoadingState
            v-else-if="store.isUploading || store.isGenerating"
            :title="store.isUploading ? '图片上传中' : 'AI 文案生成中'"
            :subtitle="store.isUploading ? '正在校验图片格式与大小...' : '正在识别图片并撰写小红书文案，请稍候...'"
          />

          <!-- Error state -->
          <ErrorState
            v-else-if="store.status === 'failed'"
            :message="store.errorMessage"
            show-retry
            @retry="onRetry"
          />

          <!-- Success result -->
          <XhsCard
            v-else-if="store.hasResult && store.result"
            :result="store.result"
            @regenerate="onRegenerate"
          />
        </section>
      </div>
    </div>

    <!-- Recent history -->
    <section
      v-if="store.history.length > 0"
      class="mt-10"
    >
      <h2 class="text-xl font-bold text-gray-900 mb-5">最近生成</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <div
          v-for="record in store.history.slice(0, 6)"
          :key="record.id"
          class="card p-4 hover:shadow-float transition-shadow cursor-pointer"
          @click="loadHistory(record)"
        >
          <div class="flex gap-4">
            <div class="w-20 h-20 rounded-xl bg-gray-100 flex-shrink-0 overflow-hidden">
              <img
                v-if="record.imageUrl"
                :src="record.imageUrl"
                alt="历史图片"
                class="w-full h-full object-cover"
              >
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-semibold text-gray-900 line-clamp-2 mb-1">
                {{ record.result?.title || '生成失败' }}
              </p>
              <p class="text-xs text-gray-400">
                {{ formatTime(record.createdAt) }}
              </p>
              <span
                class="inline-block mt-2 text-xs px-2 py-0.5 rounded-full"
                :class="record.status === 'success' ? 'bg-green-50 text-green-600' : 'bg-red-50 text-xhs-red'"
              >
                {{ record.status === 'success' ? '成功' : '失败' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useGenerationStore } from '@/stores/generation'
import type { GenerationRecord, ToneStyle } from '@/types'
import ImageUploader from '@/components/ImageUploader.vue'
import ParamForm from '@/components/ParamForm.vue'
import XhsCard from '@/components/XhsCard.vue'
import EmptyState from '@/components/EmptyState.vue'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'

const store = useGenerationStore()

const statusText = computed(() => {
  switch (store.status) {
    case 'uploading': return '上传中'
    case 'generating': return '生成中'
    case 'success': return '生成成功'
    case 'failed': return '生成失败'
    default: return ''
  }
})

const statusBadgeClass = computed(() => {
  switch (store.status) {
    case 'uploading':
    case 'generating': return 'bg-yellow-50 text-yellow-600'
    case 'success': return 'bg-green-50 text-green-600'
    case 'failed': return 'bg-red-50 text-xhs-red'
    default: return 'bg-gray-50 text-gray-500'
  }
})

function onGenerate(payload: { productName: string; targetAudience: string; toneStyle: ToneStyle }) {
  if (!store.currentImageUrl) {
    store.status = 'failed'
    store.errorMessage = '请先上传图片或输入图片链接'
    return
  }
  store.generate(payload)
}

function onRetry() {
  // Clear error and let user click generate again
  store.status = 'idle'
  store.errorMessage = ''
}

function onRegenerate() {
  // Trigger re-generation with last used params (defaults for now)
  store.generate({
    productName: '',
    targetAudience: '',
    toneStyle: '活泼'
  })
}

function loadHistory(record: GenerationRecord) {
  store.currentImageUrl = record.params.imageUrl
  store.result = record.result
  store.status = record.status === 'success' ? 'success' : 'failed'
  store.errorMessage = record.errorMessage || ''
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
</script>

<template>
  <div class="max-w-7xl mx-auto">
    <!-- Page header -->
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">文案生成</h1>
      <p class="text-gray-500">上传图片，AI 自动识别内容并生成小红书风格种草文案</p>
    </div>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8 items-stretch">
      <!-- Left column: unified input panel -->
      <section class="card p-5 sm:p-6 self-start">
        <!-- Image input section -->
        <div class="flex items-center gap-2 mb-5">
          <div class="w-8 h-8 rounded-lg bg-red-50 flex items-center justify-center">
            <svg class="w-5 h-5 text-xhs-red" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <h2 class="text-lg font-semibold text-gray-900">图片输入</h2>
        </div>
        <ImageUploader />

        <!-- Divider -->
        <div class="my-6 sm:my-8 border-t border-gray-100" />

        <!-- Params section -->
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
          :product-name="formParams.productName"
          :target-audience="formParams.targetAudience"
          :tone-style="formParams.toneStyle"
          @submit="onGenerate"
        />
      </section>

      <!-- Right column: result -->
      <div :class="store.hasResult ? 'self-start' : 'h-full'">
        <section
          v-if="!store.hasResult"
          class="card p-5 sm:p-6 h-full flex flex-col"
        >
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
              v-if="store.status !== 'idle' && !store.isUploading && store.currentImageUrl"
              class="text-xs font-medium px-2.5 py-1 rounded-full"
              :class="statusBadgeClass"
            >
              {{ statusText }}
            </span>
          </div>

          <div class="flex-1 min-h-0 flex items-center justify-center">
            <!-- Idle / uploading empty state -->
            <EmptyState
              v-if="store.status === 'idle' || store.status === 'uploading' || (store.status === 'failed' && !store.currentImageUrl)"
              title="等待生成"
              description="上传图片并填写生成参数，点击生成后即可在这里查看小红书风格文案。"
            />

            <!-- Generating -->
            <LoadingState
              v-else-if="store.isGenerating"
              title="AI 文案生成中"
              subtitle="正在识别图片并撰写小红书文案，请稍候..."
            />

            <!-- Generation error state -->
            <ErrorState
              v-else-if="store.status === 'failed' && store.currentImageUrl"
              :message="store.errorMessage"
              show-retry
              @retry="onRetry"
            />
          </div>
        </section>

        <!-- Success result -->
        <XhsCard
          v-else-if="store.hasResult && store.result"
          :result="store.result"
          @regenerate="onRegenerate"
        />
      </div>
    </div>

    <!-- Recent history -->
    <section
      v-if="historyStore.records.length > 0"
      class="mt-10"
    >
      <div class="flex items-center justify-between mb-5">
        <h2 class="text-xl font-bold text-gray-900">最近生成</h2>
        <RouterLink
          to="/workspace/history"
          class="text-sm text-xhs-red font-medium hover:text-red-700"
        >
          查看全部 →
        </RouterLink>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <div
          v-for="record in historyStore.records.slice(0, 6)"
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
import { computed, reactive } from 'vue'
import { RouterLink } from 'vue-router'
import { useGenerationStore } from '@/stores/generation'
import { useHistoryStore } from '@/stores/history'
import type { GenerationRecord, ToneStyle } from '@/types'
import ImageUploader from '@/components/ImageUploader.vue'
import ParamForm from '@/components/ParamForm.vue'
import XhsCard from '@/components/XhsCard.vue'
import EmptyState from '@/components/EmptyState.vue'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'

const store = useGenerationStore()
const historyStore = useHistoryStore()
const formParams = reactive({
  productName: store.lastParams.productName,
  targetAudience: store.lastParams.targetAudience,
  toneStyle: store.lastParams.toneStyle
})

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

async function onGenerate(payload: { productName: string; targetAudience: string; toneStyle: ToneStyle }) {
  if (!store.currentImageUrl) {
    store.status = 'failed'
    store.errorMessage = '请先上传图片或输入图片链接'
    return
  }

  await store.generate(payload)
  await historyStore.loadHistory()
}

function onRetry() {
  store.status = 'idle'
  store.errorMessage = ''
}

async function onRegenerate() {
  await store.generate({
    productName: '',
    targetAudience: '',
    toneStyle: '活泼'
  })
  await historyStore.loadHistory()
}
function loadHistory(record: GenerationRecord) {
  store.restoreRecord(record)

  // 回填生成参数（store.restoreRecord 已同步 lastParams）
  formParams.productName = store.lastParams.productName
  formParams.targetAudience = store.lastParams.targetAudience
  formParams.toneStyle = store.lastParams.toneStyle
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

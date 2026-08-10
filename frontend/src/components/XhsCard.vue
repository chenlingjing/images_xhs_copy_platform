<template>
  <div class="bg-white rounded-2xl shadow-card overflow-hidden animate-slide-up">
    <!-- Card header -->
    <div class="flex items-center justify-between px-5 py-4 border-b border-gray-50">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-full bg-gradient-to-br from-xhs-red to-pink-500 flex items-center justify-center text-white font-bold text-sm">
          AI
        </div>
        <div>
          <p class="text-sm font-semibold text-gray-900">文案助手</p>
          <p class="text-xs text-gray-400">刚刚生成</p>
        </div>
      </div>
      <span class="px-2.5 py-1 rounded-full bg-red-50 text-xhs-red text-xs font-medium">小红书</span>
    </div>

    <!-- Card body -->
    <div class="p-5 space-y-4">
      <!-- Title -->
      <div class="space-y-1.5">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-gray-400 uppercase tracking-wider">标题</span>
          <CopyButton
            :text="result.title"
            label="复制标题"
          />
        </div>
        <h2 class="text-lg font-bold text-gray-900 leading-snug">
          {{ result.title }}
        </h2>
      </div>

      <!-- Content -->
      <div class="space-y-1.5">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-gray-400 uppercase tracking-wider">正文</span>
          <CopyButton
            :text="result.content"
            label="复制正文"
          />
        </div>
        <div class="text-sm text-gray-700 leading-7 whitespace-pre-wrap">
          {{ result.content }}
        </div>
      </div>

      <!-- Tags -->
      <div class="space-y-1.5">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-gray-400 uppercase tracking-wider">话题标签</span>
          <CopyButton
            :text="result.tags.join(' ')"
            label="复制标签"
          />
        </div>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="tag in result.tags"
            :key="tag"
            class="px-3 py-1 rounded-full bg-blue-50 text-blue-600 text-sm font-medium"
          >
            {{ tag }}
          </span>
        </div>
      </div>
    </div>

    <!-- Card footer -->
    <div class="px-5 py-4 bg-gray-50 border-t border-gray-100 flex flex-col sm:flex-row gap-3">
      <button
        type="button"
        class="btn-primary flex-1"
        @click="copyFull"
      >
        <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
        </svg>
        一键复制全文
      </button>
      <button
        type="button"
        class="btn-secondary flex-1"
        @click="$emit('regenerate')"
      >
        <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        重新生成
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { GenerationResult } from '@/types'
import { copyText } from '@/utils/clipboard'
import CopyButton from './CopyButton.vue'

interface Props {
  result: GenerationResult
}

const props = defineProps<Props>()

defineEmits<{
  (e: 'regenerate'): void
}>()

async function copyFull() {
  const { title, content, tags } = props.result
  const fullText = `${title}\n\n${content}\n\n${tags.join(' ')}`
  try {
    await copyText(fullText)
    alert('全文已复制到剪贴板')
  } catch {
    alert('复制失败，请手动复制')
  }
}
</script>

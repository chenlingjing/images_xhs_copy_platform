<template>
  <form
    class="space-y-5"
    @submit.prevent="handleSubmit"
  >
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">产品名称（可选）</label>
      <input
        v-model="form.productName"
        type="text"
        placeholder="例如：丝绒奶茶"
        class="input"
      >
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">目标人群（可选）</label>
      <input
        v-model="form.targetAudience"
        type="text"
        placeholder="例如：18-25 岁学生党"
        class="input"
      >
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-3">语气风格</label>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="tone in toneOptions"
          :key="tone"
          type="button"
          class="px-4 py-2 rounded-full text-sm font-medium border transition-all"
          :class="form.toneStyle === tone
            ? 'border-xhs-red text-xhs-red bg-red-50'
            : 'border-gray-200 text-gray-600 bg-white hover:border-gray-300'"
          @click="form.toneStyle = tone"
        >
          {{ tone }}
        </button>
      </div>
    </div>

    <button
      type="submit"
      class="btn-primary w-full text-base py-3.5"
      :disabled="disabled || isGenerating"
      :title="disabled ? '请先上传图片' : ''"
    >
      <svg
        v-if="isGenerating"
        class="animate-spin -ml-1 mr-2 h-5 w-5 text-white"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
      </svg>
      {{ isGenerating ? 'AI 生成中...' : '生成小红书文案' }}
    </button>
  </form>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import type { ToneStyle } from '@/types'

interface Props {
  disabled?: boolean
  isGenerating?: boolean
}

withDefaults(defineProps<Props>(), {
  disabled: false,
  isGenerating: false
})

const toneOptions: ToneStyle[] = ['活泼', '温柔', '专业', '搞笑', '治愈']

const form = reactive({
  productName: '',
  targetAudience: '',
  toneStyle: '活泼' as ToneStyle
})

const emit = defineEmits<{
  (e: 'submit', payload: { productName: string; targetAudience: string; toneStyle: ToneStyle }): void
}>()

function handleSubmit() {
  emit('submit', { ...form })
}
</script>

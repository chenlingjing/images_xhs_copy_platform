<template>
  <button
    type="button"
    class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all focus:outline-none"
    :class="copied
      ? 'bg-green-50 text-green-600'
      : 'bg-gray-50 text-gray-600 hover:bg-gray-100 hover:text-gray-900'"
    @click="handleCopy"
  >
    <svg v-if="!copied" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
    </svg>
    <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 13l4 4L19 7" />
    </svg>
    {{ copied ? '已复制' : label }}
  </button>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { copyText } from '@/utils/clipboard'

interface Props {
  text: string
  label?: string
}

const props = withDefaults(defineProps<Props>(), {
  label: '复制'
})

const copied = ref(false)

async function handleCopy() {
  try {
    await copyText(props.text)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch {
    alert('复制失败，请手动复制')
  }
}
</script>

<template>
  <div class="flex flex-col items-center justify-center py-12 px-6 text-center animate-fade-in">
    <div class="w-16 h-16 rounded-2xl bg-red-50 flex items-center justify-center mb-4">
      <svg class="w-8 h-8 text-xhs-red" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
    </div>
    <h3 class="text-base font-semibold text-gray-900 mb-2">{{ title }}</h3>
    <p class="text-sm text-red-500 max-w-sm leading-relaxed mb-5">{{ message }}</p>
    <button
      v-if="showRetry"
      type="button"
      class="btn-secondary text-sm"
      @click="$emit('retry')"
    >
      重试
    </button>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title?: string
  message: string
  showRetry?: boolean
}

withDefaults(defineProps<Props>(), {
  title: '出错了',
  showRetry: false
})

defineEmits<{
  (e: 'retry'): void
}>()
</script>

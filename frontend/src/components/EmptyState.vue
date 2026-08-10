<template>
  <div class="flex flex-col items-center justify-center py-14 px-6 text-center animate-fade-in">
    <div class="w-20 h-20 rounded-2xl bg-gray-50 flex items-center justify-center mb-5">
      <svg class="w-10 h-10 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
      </svg>
    </div>
    <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ title }}</h3>
    <p class="text-sm text-gray-500 max-w-xs leading-relaxed">{{ description }}</p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title?: string
  description?: string
}

withDefaults(defineProps<Props>(), {
  title: '暂无内容',
  description: '上传图片后，AI 将为你生成小红书风格种草文案。'
})
</script>

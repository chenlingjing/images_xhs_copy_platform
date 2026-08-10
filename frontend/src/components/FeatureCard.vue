<template>
  <div class="card p-6 hover:shadow-float transition-shadow">
    <div class="w-12 h-12 rounded-xl bg-red-50 flex items-center justify-center mb-5">
      <svg
        class="w-6 h-6 text-xhs-red"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        v-html="iconSvg"
      />
    </div>
    <h3 class="text-lg font-bold text-gray-900 mb-2">{{ title }}</h3>
    <p class="text-sm text-gray-500 leading-relaxed">{{ description }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  icon: 'upload' | 'sparkles' | 'copy'
  title: string
  description: string
}

const props = defineProps<Props>()

const iconSvg = computed(() => {
  const paths: Record<Props['icon'], string> = {
    upload: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />',
    sparkles: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />',
    copy: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />'
  }
  return paths[props.icon]
})
</script>

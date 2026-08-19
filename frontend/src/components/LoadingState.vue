<template>
  <div class="flex flex-col items-center justify-center py-12 animate-fade-in">
    <div class="relative w-16 h-16 mb-5">
      <div class="absolute inset-0 rounded-full border-4 border-gray-100"></div>
      <div class="absolute inset-0 rounded-full border-4 border-xhs-red border-t-transparent animate-spin"></div>
      <div class="absolute inset-0 flex items-center justify-center">
        <div class="w-2 h-2 rounded-full bg-xhs-red animate-pulse"></div>
      </div>
    </div>
    <p class="text-gray-700 font-medium text-base">{{ title }}</p>
    <p v-if="subtitle" class="text-gray-400 text-sm mt-1">{{ subtitle }}</p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title?: string
  subtitle?: string
}

withDefaults(defineProps<Props>(), {
  title: '处理中...',
  subtitle: ''
})
</script>

<template>
  <div class="card overflow-hidden">
    <button
      type="button"
      class="w-full flex items-center justify-between p-5 text-left hover:bg-gray-50 transition-colors"
      @click="isOpen = !isOpen"
    >
      <span class="font-semibold text-gray-900">{{ question }}</span>
      <svg
        class="w-5 h-5 text-gray-400 transition-transform duration-200 flex-shrink-0 ml-4"
        :class="{ 'rotate-180': isOpen }"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>
    <div
      v-show="isOpen"
      class="px-5 pb-5 text-sm text-gray-500 leading-relaxed"
    >
      {{ answer }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  question: string
  answer: string
}

defineProps<Props>()

const isOpen = ref(false)
</script>

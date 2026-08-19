<template>
  <div class="bg-white rounded-2xl sm:rounded-3xl shadow-2xl border border-gray-100 overflow-hidden w-full max-w-[340px] sm:max-w-[400px]">
    <!-- Card header / author -->
    <div class="flex items-center gap-3 px-4 sm:px-5 pt-4 sm:pt-5 pb-3">
      <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-full bg-gradient-to-br from-xhs-red to-pink-400 flex items-center justify-center text-white font-bold text-sm">
        AI
      </div>
      <div>
        <p class="text-sm font-bold text-gray-900">种草小助手</p>
        <p class="text-xs text-gray-400">刚刚发布</p>
      </div>
      <button class="ml-auto text-gray-300 hover:text-xhs-red transition-colors">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
        </svg>
      </button>
    </div>

    <!-- Image -->
    <div class="aspect-square bg-gradient-to-br from-red-50 to-pink-50 flex items-center justify-center">
      <img
        :src="imageUrl"
        alt="示例图片"
        class="w-full h-full object-cover"
      >
    </div>

    <!-- Content -->
    <div class="px-4 sm:px-5 py-4">
      <h3 class="text-base sm:text-lg font-bold text-gray-900 mb-2 line-clamp-2">
        {{ result.title }}
      </h3>
      <p class="text-sm text-gray-600 line-clamp-4 mb-3 leading-relaxed">
        {{ result.content }}
      </p>
      <div class="flex flex-wrap gap-2 mb-4">
        <span
          v-for="tag in result.tags"
          :key="tag"
          class="text-xs text-blue-600 font-medium"
        >
          {{ tag }}
        </span>
      </div>

      <!-- Actions -->
      <div class="flex items-center gap-5 text-gray-400 text-sm">
        <div class="flex items-center gap-1">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
          <span>1.2k</span>
        </div>
        <div class="flex items-center gap-1">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <span>328</span>
        </div>
        <div class="flex items-center gap-1">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
          </svg>
          <span>分享</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  imageUrl: string
  result: {
    title: string
    content: string
    tags: string[]
  }
}

defineProps<Props>()
</script>

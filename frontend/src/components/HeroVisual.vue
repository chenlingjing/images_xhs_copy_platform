<template>
  <div class="relative w-full max-w-3xl mx-auto h-[380px] sm:h-[460px] lg:h-[520px]">
    <!-- Background grid -->
    <div class="absolute inset-0 rounded-3xl bg-gradient-to-br from-red-50 via-pink-50 to-rose-50 border border-red-100 overflow-hidden">
      <div
        class="absolute inset-0 opacity-30"
        style="background-image: linear-gradient(#ff2442 1px, transparent 1px), linear-gradient(90deg, #ff2442 1px, transparent 1px); background-size: 40px 40px;"
      />
    </div>

    <!-- Decorative blobs -->
    <div class="absolute -top-10 -right-10 w-40 h-40 bg-red-200 rounded-full blur-3xl opacity-40" />
    <div class="absolute -bottom-10 -left-10 w-48 h-48 bg-pink-200 rounded-full blur-3xl opacity-40" />

    <!-- Center note card -->
    <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[86%] sm:w-auto z-10">
      <HeroNoteCard
        :image-url="imageUrl"
        :result="result"
      />
    </div>

    <!-- Floating badge: AI image recognition -->
    <div class="absolute top-6 sm:top-10 left-4 sm:left-8 bg-white rounded-xl shadow-lg px-3 py-2 sm:px-4 sm:py-2.5 flex items-center gap-2 animate-float">
      <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-red-50 flex items-center justify-center">
        <svg class="w-4 h-4 sm:w-5 sm:h-5 text-xhs-red" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
        </svg>
      </div>
      <span class="text-xs sm:text-sm font-semibold text-gray-800">AI 图片识别</span>
    </div>

    <!-- Floating badge: 3min delivery -->
    <div class="absolute top-16 sm:top-24 right-4 sm:right-8 bg-white rounded-xl shadow-lg px-3 py-2 sm:px-4 sm:py-2.5 flex items-center gap-2 animate-float" style="animation-delay: 1s;">
      <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-orange-50 flex items-center justify-center">
        <svg class="w-4 h-4 sm:w-5 sm:h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      </div>
      <div>
        <p class="text-xs sm:text-sm font-bold text-gray-800">3 分钟</p>
        <p class="text-[10px] sm:text-xs text-gray-500">快速出稿</p>
      </div>
    </div>

    <!-- Floating badge: +35% exposure -->
    <div class="absolute bottom-20 sm:bottom-24 left-2 sm:left-6 bg-xhs-red text-white rounded-xl shadow-lg px-3 py-2 sm:px-4 sm:py-2.5 animate-float" style="animation-delay: 0.5s;">
      <p class="text-lg sm:text-2xl font-bold">+35%</p>
      <p class="text-[10px] sm:text-xs opacity-90">笔记曝光提升</p>
    </div>

    <!-- Floating badge: auto tags -->
    <div class="absolute bottom-8 sm:bottom-12 right-4 sm:right-10 bg-white rounded-xl shadow-lg px-3 py-2 sm:px-4 sm:py-2.5 flex items-center gap-2 animate-float" style="animation-delay: 1.5s;">
      <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-blue-50 flex items-center justify-center">
        <svg class="w-4 h-4 sm:w-5 sm:h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
        </svg>
      </div>
      <span class="text-xs sm:text-sm font-semibold text-gray-800">自动话题标签</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import HeroNoteCard from './HeroNoteCard.vue'

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

<style scoped>
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.animate-float {
  animation: float 4s ease-in-out infinite;
}
</style>

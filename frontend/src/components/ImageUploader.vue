<template>
  <div class="space-y-4">
    <!-- Tabs -->
    <div class="flex p-1 bg-gray-100 rounded-xl">
      <button
        type="button"
        class="flex-1 py-2 text-sm font-medium rounded-lg transition-all"
        :class="activeTab === 'upload' ? 'bg-white text-xhs-red shadow-sm' : 'text-gray-500 hover:text-gray-700'"
        @click="activeTab = 'upload'"
      >
        本地上传
      </button>
      <button
        type="button"
        class="flex-1 py-2 text-sm font-medium rounded-lg transition-all"
        :class="activeTab === 'url' ? 'bg-white text-xhs-red shadow-sm' : 'text-gray-500 hover:text-gray-700'"
        @click="activeTab = 'url'"
      >
        图片链接
      </button>
    </div>

    <!-- Upload area -->
    <div
      v-if="activeTab === 'upload'"
      class="relative"
    >
      <div
        v-if="!previewUrl"
        class="group relative border-2 border-dashed border-gray-200 rounded-2xl p-8 text-center transition-all cursor-pointer hover:border-xhs-red/40 hover:bg-red-50/30"
        :class="{ 'border-xhs-red bg-red-50/20': isDragging }"
        @dragenter.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @dragover.prevent
        @drop.prevent="handleDrop"
        @click="triggerFileInput"
      >
        <input
          ref="fileInput"
          type="file"
          accept="image/jpeg,image/png,image/webp,image/gif"
          class="hidden"
          @change="handleFileChange"
        >
        <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-red-50 flex items-center justify-center group-hover:scale-105 transition-transform">
          <svg class="w-8 h-8 text-xhs-red" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <p class="text-base font-medium text-gray-900 mb-1">点击或拖拽上传图片</p>
        <p class="text-sm text-gray-500">支持 jpg / png / webp / gif，最大 10MB</p>
      </div>

      <div
        v-else
        class="relative rounded-2xl overflow-hidden bg-gray-100 border border-gray-100 flex items-center justify-center"
      >
        <img
          :src="previewUrl"
          alt="预览图"
          class="max-w-full max-h-[480px] object-contain"
        >
        <button
          type="button"
          class="absolute top-3 right-3 w-8 h-8 rounded-full bg-black/50 text-white flex items-center justify-center hover:bg-black/70 transition-colors"
          @click="removeImage"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- URL input -->
    <div
      v-else
      class="space-y-4"
    >
      <div class="flex gap-2">
        <input
          v-model="imageUrl"
          type="text"
          placeholder="粘贴图片链接，例如 https://example.com/image.jpg"
          class="input"
          @keyup.enter="handleUrlSubmit"
        >
        <button
          type="button"
          class="btn-primary whitespace-nowrap"
          :disabled="!imageUrl.trim() || isUploading"
          @click="handleUrlSubmit"
        >
          加载
        </button>
      </div>

      <div
        v-if="previewUrl"
        class="relative rounded-2xl overflow-hidden bg-gray-100 border border-gray-100 flex items-center justify-center"
      >
        <img
          :src="previewUrl"
          alt="预览图"
          class="max-w-full max-h-[480px] object-contain"
        >
        <button
          type="button"
          class="absolute top-3 right-3 w-8 h-8 rounded-full bg-black/50 text-white flex items-center justify-center hover:bg-black/70 transition-colors"
          @click="removeImage"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useGenerationStore } from '@/stores/generation'

const store = useGenerationStore()
const activeTab = ref<'upload' | 'url'>('upload')
const fileInput = ref<HTMLInputElement | null>(null)
const isDragging = ref(false)
const imageUrl = ref('')

const previewUrl = computed(() => store.currentImageUrl)
const isUploading = computed(() => store.isUploading)

function triggerFileInput() {
  fileInput.value?.click()
}

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    store.uploadLocalImage(file)
  }
}

function handleDrop(event: DragEvent) {
  isDragging.value = false
  const file = event.dataTransfer?.files[0]
  if (file) {
    store.uploadLocalImage(file)
  }
}

async function handleUrlSubmit() {
  if (!imageUrl.value.trim()) return
  await store.loadImageUrl(imageUrl.value)
}

function removeImage() {
  store.clearImage()
  imageUrl.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
</script>

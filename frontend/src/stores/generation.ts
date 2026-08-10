import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { GenerationParams, GenerationRecord, GenerationResult, GenerationStatus } from '@/types'
import { uploadImage, uploadImageFromUrl, generateCopy } from '@/services/mockApi'

export const useGenerationStore = defineStore('generation', () => {
  const currentImageUrl = ref('')
  const status = ref<GenerationStatus>('idle')
  const result = ref<GenerationResult | null>(null)
  const errorMessage = ref('')
  const history = ref<GenerationRecord[]>([])

  const isUploading = computed(() => status.value === 'uploading')
  const isGenerating = computed(() => status.value === 'generating')
  const isBusy = computed(() => isUploading.value || isGenerating.value)
  const hasResult = computed(() => status.value === 'success' && result.value !== null)

  async function uploadLocalImage(file: File) {
    status.value = 'uploading'
    errorMessage.value = ''
    result.value = null

    try {
      const res = await uploadImage(file)
      currentImageUrl.value = res.url
      status.value = 'idle'
    } catch (err) {
      status.value = 'failed'
      errorMessage.value = err instanceof Error ? err.message : '图片上传失败'
      throw err
    }
  }

  async function loadImageUrl(url: string) {
    status.value = 'uploading'
    errorMessage.value = ''
    result.value = null

    try {
      const res = await uploadImageFromUrl(url)
      currentImageUrl.value = res.url
      status.value = 'idle'
    } catch (err) {
      status.value = 'failed'
      errorMessage.value = err instanceof Error ? err.message : '图片链接加载失败'
      throw err
    }
  }

  function clearImage() {
    currentImageUrl.value = ''
    result.value = null
    status.value = 'idle'
    errorMessage.value = ''
  }

  async function generate(params: Omit<GenerationParams, 'imageUrl'>) {
    if (!currentImageUrl.value) {
      errorMessage.value = '请先上传图片或输入图片链接'
      status.value = 'failed'
      return
    }

    status.value = 'generating'
    errorMessage.value = ''
    result.value = null

    try {
      const generationResult = await generateCopy({
        imageUrl: currentImageUrl.value,
        ...params
      })

      result.value = generationResult
      status.value = 'success'

      const record: GenerationRecord = {
        id: generationResult.id,
        imageUrl: currentImageUrl.value,
        params: { imageUrl: currentImageUrl.value, ...params },
        result: generationResult,
        status: 'success',
        createdAt: new Date().toISOString()
      }

      history.value.unshift(record)
    } catch (err) {
      status.value = 'failed'
      errorMessage.value = err instanceof Error ? err.message : '文案生成失败，请重试'

      const record: GenerationRecord = {
        id: `failed-${Date.now()}`,
        imageUrl: currentImageUrl.value,
        params: { imageUrl: currentImageUrl.value, ...params },
        result: null,
        status: 'failed',
        errorMessage: errorMessage.value,
        createdAt: new Date().toISOString()
      }

      history.value.unshift(record)
    }
  }

  return {
    currentImageUrl,
    status,
    result,
    errorMessage,
    history,
    isUploading,
    isGenerating,
    isBusy,
    hasResult,
    uploadLocalImage,
    loadImageUrl,
    clearImage,
    generate
  }
})

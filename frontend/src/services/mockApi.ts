import type { GenerationParams, GenerationResult, MockUploadResponse } from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8081'

type ApiEnvelope<T> = {
  code: number
  message: string
  data: T | null
}

function toAbsoluteUrl(rawUrl: string) {
  if (!rawUrl) return rawUrl
  if (/^https?:\/\//i.test(rawUrl)) return rawUrl
  if (rawUrl.startsWith('/')) return `${API_BASE_URL}${rawUrl}`
  return `${API_BASE_URL}/${rawUrl.replace(/^\/+/, '')}`
}

function toServerImageUrl(rawUrl: string) {
  if (!rawUrl) return rawUrl
  if (rawUrl.startsWith(API_BASE_URL)) return rawUrl.replace(API_BASE_URL, '')
  return rawUrl
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      ...(init.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }),
      ...(init.headers || {})
    }
  })

  const payload = (await response.json()) as ApiEnvelope<T>

  if (!response.ok || payload.code !== 200) {
    throw new Error(payload.message || '请求失败')
  }

  if (payload.data === null || payload.data === undefined) {
    return null as T
  }

  return payload.data as T
}

export async function uploadImage(file: File): Promise<MockUploadResponse> {
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif', 'image/bmp']
  const fileExt = (file.name || '').split('.').pop()?.toLowerCase() || ''
  const mimeOk = allowedTypes.includes(file.type) || ['jpg', 'jpeg', 'png', 'webp', 'gif', 'bmp'].includes(fileExt)

  if (!mimeOk) {
    throw new Error('图片格式不支持，请上传 jpg / png / webp / gif / bmp 格式的图片')
  }

  if (file.size > 10 * 1024 * 1024) {
    throw new Error('图片大小超过 10MB，请压缩后重试')
  }

  const formData = new FormData()
  formData.append('file', file)

  const data = await request<{ image_url: string; filename: string }>('/images/upload', {
    method: 'POST',
    body: formData
  })

  return {
    url: toAbsoluteUrl(data.image_url)
  }
}

export async function uploadImageFromUrl(url: string): Promise<MockUploadResponse> {
  const trimmed = url.trim()
  if (!trimmed) {
    throw new Error('请输入图片链接')
  }

  await request<{ valid: boolean; content_type?: string; content_length?: number }>(
    `/images/validate-url?image_url=${encodeURIComponent(trimmed)}`,
    { method: 'POST' }
  )

  return { url: trimmed }
}

export async function generateCopy(params: GenerationParams): Promise<GenerationResult> {
  const rawImageUrl = params.imageUrl || ''
  const isLocalImage = /\/uploads\//i.test(rawImageUrl) || rawImageUrl.startsWith(API_BASE_URL)

  const payload = {
    imageType: isLocalImage ? 1 : 2,
    imageUrl: isLocalImage ? toServerImageUrl(rawImageUrl) : rawImageUrl,
    productName: params.productName || '',
    targetAudience: params.targetAudience || '',
    toneStyle: params.toneStyle || '活泼'
  }

  const data = await request<{
    id: number
    title: string
    content: string
    tags: string[]
  }>('/api/generate', {
    method: 'POST',
    body: JSON.stringify(payload)
  })

  return {
    id: String(data.id),
    title: data.title,
    content: data.content,
    tags: data.tags || []
  }
}

import type {
  GenerationParams,
  GenerationRecord,
  GenerationResult,
  MockUploadResponse
} from '@/types'
import { request, toAbsoluteUrl, toServerImageUrl } from './api'

type ApiGenerationRecord = {
  id: number
  imageType: number
  imageUrl: string
  productName: string
  targetAudience: string
  toneStyle: string
  title: string
  content: string
  tags: string[]
  status: 'pending' | 'success' | 'failed'
  errorMessage: string
  durationMs: number
  createTime: string
}

type PageResponse<T> = {
  total: number
  page: number
  pageSize: number
  items: T[]
}

function mapRecord(record: ApiGenerationRecord): GenerationRecord {
  const status = record.status === 'success' ? 'success' : 'failed'
  return {
    id: String(record.id),
    imageUrl: toAbsoluteUrl(record.imageUrl),
    params: {
      imageUrl: toAbsoluteUrl(record.imageUrl),
      productName: record.productName,
      targetAudience: record.targetAudience,
      toneStyle: record.toneStyle as GenerationParams['toneStyle']
    },
    result: status === 'success'
      ? {
          id: String(record.id),
          title: record.title,
          content: record.content,
          tags: record.tags || []
        }
      : null,
    status,
    errorMessage: record.errorMessage || undefined,
    createdAt: record.createTime
  }
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
  return { url: toAbsoluteUrl(data.image_url) }
}

export async function uploadImageFromUrl(url: string): Promise<MockUploadResponse> {
  const trimmed = url.trim()
  if (!trimmed) {
    throw new Error('请输入图片链接')
  }
  await request<{ valid: boolean }>(
    `/images/validate-url?image_url=${encodeURIComponent(trimmed)}`,
    { method: 'POST' }
  )
  return { url: trimmed }
}

export async function generateCopy(params: GenerationParams): Promise<GenerationResult> {
  const rawImageUrl = params.imageUrl || ''
  const isLocalImage = /\/uploads\//i.test(rawImageUrl)
  const data = await request<{ id: number; title: string; content: string; tags: string[] }>(
    '/api/generate',
    {
      method: 'POST',
      body: JSON.stringify({
        imageType: isLocalImage ? 1 : 2,
        imageUrl: isLocalImage ? toServerImageUrl(rawImageUrl) : rawImageUrl,
        productName: params.productName || '',
        targetAudience: params.targetAudience || '',
        toneStyle: params.toneStyle || '活泼'
      })
    }
  )

  return {
    id: String(data.id),
    title: data.title,
    content: data.content,
    tags: data.tags || []
  }
}

export async function getGenerationRecords(): Promise<GenerationRecord[]> {
  const page = await request<PageResponse<ApiGenerationRecord>>(
    '/api/generate/records?page=1&pageSize=100'
  )
  return page.items.map(mapRecord)
}

export async function deleteGenerationRecord(id: string) {
  await request<null>(`/api/generate/records/${encodeURIComponent(id)}`, {
    method: 'DELETE'
  })
}

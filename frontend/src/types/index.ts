export type GenerationStatus = 'idle' | 'uploading' | 'generating' | 'success' | 'failed'

export type ToneStyle = '活泼' | '温柔' | '专业' | '搞笑' | '治愈'

export interface GenerationParams {
  imageUrl: string
  productName?: string
  targetAudience?: string
  toneStyle?: ToneStyle
}

export interface GenerationResult {
  id: string
  title: string
  content: string
  tags: string[]
}

export interface GenerationRecord {
  id: string
  imageUrl: string
  params: GenerationParams
  result: GenerationResult | null
  status: Exclude<GenerationStatus, 'idle'>
  errorMessage?: string
  createdAt: string
}

export interface MockUploadResponse {
  url: string
}

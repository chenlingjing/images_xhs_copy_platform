export type GenerationStatus = 'idle' | 'uploading' | 'generating' | 'success' | 'failed'

export type ToneStyle = '活泼' | '温柔' | '专业' | '搞笑' | '治愈'

export type UserRole = 'user' | 'admin'

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

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
    requiresAdmin?: boolean
    requiresGuest?: boolean
  }
}

export interface User {
  id: string
  username: string
  email: string
  role: UserRole
  password?: string
  avatar?: string
  createdAt: string
  lastActiveAt: string
}

export interface DailyStats {
  date: string
  totalGenerations: number
  successCount: number
  failedCount: number
  uniqueUsers: number
}

export interface AdminOverview {
  totalUsers: number
  totalGenerations: number
  todayGenerations: number
  successRate: number
  avgGenerationTimeMs: number
  dailyStats: DailyStats[]
}

export interface AdminGenerationRecord extends GenerationRecord {
  user: Pick<User, 'id' | 'username' | 'avatar'>
}

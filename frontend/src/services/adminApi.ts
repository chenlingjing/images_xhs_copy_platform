import type {
  AdminGenerationRecord,
  AdminOverview,
  GenerationParams,
  User
} from '@/types'
import { request, toAbsoluteUrl } from './api'

type ApiUser = Omit<User, 'id'> & { id: number }

type ApiAdminGeneration = {
  id: number
  imageUrl: string
  params: GenerationParams
  result: {
    id: number
    title: string
    content: string
    tags: string[]
  } | null
  status: 'success' | 'failed'
  errorMessage: string
  createdAt: string
  user: {
    id: number
    username: string
    avatar?: string
  }
}

function mapUser(user: ApiUser): User {
  return {
    ...user,
    id: String(user.id),
    avatar: toAbsoluteUrl(user.avatar || '')
  }
}

export async function getAdminOverview(): Promise<AdminOverview> {
  return request<AdminOverview>('/api/admin/overview')
}

export async function getUsers(): Promise<User[]> {
  const users = await request<ApiUser[]>('/api/admin/users')
  return users.map(mapUser)
}

export async function getGenerations(): Promise<AdminGenerationRecord[]> {
  const records = await request<ApiAdminGeneration[]>('/api/admin/generations?pageSize=500')
  return records.map(record => ({
    id: String(record.id),
    imageUrl: toAbsoluteUrl(record.imageUrl),
    params: {
      ...record.params,
      imageUrl: toAbsoluteUrl(record.params.imageUrl)
    },
    result: record.result
      ? {
          ...record.result,
          id: String(record.result.id)
        }
      : null,
    status: record.status,
    errorMessage: record.errorMessage || undefined,
    createdAt: record.createdAt,
    user: {
      id: String(record.user.id),
      username: record.user.username,
      avatar: toAbsoluteUrl(record.user.avatar || '')
    }
  }))
}

export async function deleteGeneration(id: string): Promise<void> {
  await request<null>(`/api/admin/generations/${encodeURIComponent(id)}`, {
    method: 'DELETE'
  })
}

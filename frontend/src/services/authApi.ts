import type { User } from '@/types'
import { request, toAbsoluteUrl, toServerImageUrl } from './api'

type ApiUser = Omit<User, 'id'> & { id: number }

type AuthResult = {
  token: string
  user: ApiUser
}

function mapUser(user: ApiUser): User {
  return {
    ...user,
    id: String(user.id),
    avatar: toAbsoluteUrl(user.avatar || '')
  }
}

export async function loginUser(account: string, password: string) {
  const result = await request<AuthResult>('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ account, password })
  })
  return { token: result.token, user: mapUser(result.user) }
}

export async function registerUser(username: string, email: string, password: string) {
  const result = await request<AuthResult>('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify({ username, email, password })
  })
  return { token: result.token, user: mapUser(result.user) }
}

export async function getCurrentUser() {
  const user = await request<ApiUser>('/api/auth/me')
  return mapUser(user)
}

export async function logoutUser() {
  await request<null>('/api/auth/logout', { method: 'POST' })
}

export async function updateUserAvatar(avatar: string) {
  const user = await request<ApiUser>('/api/auth/avatar', {
    method: 'PATCH',
    body: JSON.stringify({ avatar: toServerImageUrl(avatar) })
  })
  return mapUser(user)
}

export async function changeUserPassword(oldPassword: string, newPassword: string) {
  await request<null>('/api/auth/change-password', {
    method: 'POST',
    body: JSON.stringify({ oldPassword, newPassword })
  })
}

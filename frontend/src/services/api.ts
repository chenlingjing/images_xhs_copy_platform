export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'

const TOKEN_KEY = 'xhs_auth_token'
const USER_KEY = 'xhs_auth_user'

type ApiEnvelope<T> = {
  code: number
  message: string
  data: T | null
}

export function getAuthToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function setAuthToken(token: string | null) {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token)
  } else {
    localStorage.removeItem(TOKEN_KEY)
  }
}

export function clearStoredAuth() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}

export async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers)
  if (!(init.body instanceof FormData) && init.body !== undefined) {
    headers.set('Content-Type', 'application/json')
  }

  const token = getAuthToken()
  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers
  })

  let payload: ApiEnvelope<T>
  try {
    payload = (await response.json()) as ApiEnvelope<T>
  } catch {
    throw new Error('服务器响应格式错误')
  }

  if (!response.ok || payload.code !== 200) {
    if (payload.code === 401 || response.status === 401) {
      clearStoredAuth()
      window.dispatchEvent(new CustomEvent('auth:unauthorized'))
    }
    throw new Error(payload.message || '请求失败')
  }

  return payload.data as T
}

export function toAbsoluteUrl(rawUrl: string) {
  if (!rawUrl) return rawUrl
  if (/^https?:\/\//i.test(rawUrl)) return rawUrl
  if (rawUrl.startsWith('/')) return `${API_BASE_URL}${rawUrl}`
  return `${API_BASE_URL}/${rawUrl.replace(/^\/+/, '')}`
}

export function toServerImageUrl(rawUrl: string) {
  if (!rawUrl) return rawUrl
  if (rawUrl.startsWith(API_BASE_URL)) return rawUrl.replace(API_BASE_URL, '')
  return rawUrl
}

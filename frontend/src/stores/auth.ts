import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import type { User } from '@/types'
import {
  changeUserPassword,
  getCurrentUser,
  loginUser,
  logoutUser,
  registerUser,
  updateUserAvatar
} from '@/services/authApi'
import { clearStoredAuth, getAuthToken, setAuthToken } from '@/services/api'

const AUTH_USER_KEY = 'xhs_auth_user'

export interface LoginCredentials {
  account: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
}

function getStoredUser(): User | null {
  try {
    const raw = localStorage.getItem(AUTH_USER_KEY)
    return raw ? JSON.parse(raw) as User : null
  } catch {
    localStorage.removeItem(AUTH_USER_KEY)
    return null
  }
}

export const useAuthStore = defineStore('auth', () => {
  const currentUser = ref<User | null>(getStoredUser())
  const initialized = ref(false)

  const isLoggedIn = computed(() => currentUser.value !== null && Boolean(getAuthToken()))
  const isAdmin = computed(() => currentUser.value?.role === 'admin')
  const userRole = computed(() => currentUser.value?.role ?? null)

  function persistUser(user: User | null) {
    currentUser.value = user
    if (user) {
      localStorage.setItem(AUTH_USER_KEY, JSON.stringify(user))
    } else {
      localStorage.removeItem(AUTH_USER_KEY)
    }
  }

  function establishSession(token: string, user: User) {
    setAuthToken(token)
    persistUser(user)
  }

  async function initialize() {
    if (initialized.value) return
    if (!getAuthToken()) {
      persistUser(null)
      initialized.value = true
      return
    }

    try {
      persistUser(await getCurrentUser())
    } catch {
      clearStoredAuth()
      currentUser.value = null
    } finally {
      initialized.value = true
    }
  }

  async function login(credentials: LoginCredentials): Promise<{ success: boolean; message?: string }> {
    try {
      const result = await loginUser(credentials.account, credentials.password)
      establishSession(result.token, result.user)
      return { success: true }
    } catch (error) {
      return {
        success: false,
        message: error instanceof Error ? error.message : '登录失败'
      }
    }
  }

  async function register(data: RegisterData): Promise<{ success: boolean; message?: string }> {
    try {
      const result = await registerUser(data.username, data.email, data.password)
      establishSession(result.token, result.user)
      return { success: true }
    } catch (error) {
      return {
        success: false,
        message: error instanceof Error ? error.message : '注册失败'
      }
    }
  }

  async function logout() {
    try {
      if (getAuthToken()) {
        await logoutUser()
      }
    } catch {
      // Local logout must still complete when the session is already invalid.
    } finally {
      clearStoredAuth()
      currentUser.value = null
    }
  }

  async function updateAvatar(avatarUrl: string) {
    persistUser(await updateUserAvatar(avatarUrl))
  }

  async function changePassword(
    oldPassword: string,
    newPassword: string
  ): Promise<{ success: boolean; message?: string }> {
    try {
      await changeUserPassword(oldPassword, newPassword)
      return { success: true }
    } catch (error) {
      return {
        success: false,
        message: error instanceof Error ? error.message : '密码修改失败'
      }
    }
  }

  window.addEventListener('auth:unauthorized', () => {
    currentUser.value = null
  })

  return {
    currentUser,
    initialized,
    isLoggedIn,
    isAdmin,
    userRole,
    initialize,
    login,
    register,
    logout,
    updateAvatar,
    changePassword
  }
})

import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { User, UserRole } from '@/types'

const AUTH_KEY = 'xhs_auth_user'
const USERS_KEY = 'xhs_users'

function getStoredUsers(): User[] {
  try {
    return JSON.parse(localStorage.getItem(USERS_KEY) || '[]')
  } catch {
    return []
  }
}

function saveUsers(users: User[]) {
  localStorage.setItem(USERS_KEY, JSON.stringify(users))
}

function seedInitialUsers() {
  const users = getStoredUsers()
  if (users.length === 0) {
    const initialUsers: User[] = [
      {
        id: 'admin-1',
        username: 'admin',
        email: 'admin@example.com',
        role: 'admin',
        password: 'admin123',
        avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=admin',
        createdAt: '2026-01-01T00:00:00.000Z',
        lastActiveAt: new Date().toISOString()
      },
      {
        id: 'user-1',
        username: 'demo',
        email: 'demo@example.com',
        role: 'user',
        password: 'demo123',
        avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=demo',
        createdAt: '2026-08-01T00:00:00.000Z',
        lastActiveAt: new Date().toISOString()
      }
    ]
    saveUsers(initialUsers)
  }
}

seedInitialUsers()

export interface LoginCredentials {
  account: string // username or email
  password: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
}

export const useAuthStore = defineStore('auth', () => {
  const currentUser = ref<User | null>(null)

  // Initialize from localStorage
  const saved = localStorage.getItem(AUTH_KEY)
  if (saved) {
    try {
      currentUser.value = JSON.parse(saved)
    } catch {
      localStorage.removeItem(AUTH_KEY)
    }
  }

  const isLoggedIn = computed(() => currentUser.value !== null)
  const isAdmin = computed(() => currentUser.value?.role === 'admin')
  const userRole = computed(() => currentUser.value?.role ?? null)

  function persist(user: User | null) {
    if (user) {
      localStorage.setItem(AUTH_KEY, JSON.stringify(user))
    } else {
      localStorage.removeItem(AUTH_KEY)
    }
  }

  function updateLastActive() {
    if (currentUser.value) {
      currentUser.value.lastActiveAt = new Date().toISOString()
      persist(currentUser.value)
    }
  }

  function login(credentials: LoginCredentials): { success: boolean; message?: string } {
    const users = getStoredUsers()
    const user = users.find(
      u =>
        (u.username === credentials.account || u.email === credentials.account) &&
        u.password === credentials.password
    )

    if (!user) {
      return { success: false, message: '用户名/邮箱或密码错误' }
    }

    user.lastActiveAt = new Date().toISOString()
    saveUsers(users)
    currentUser.value = user
    persist(user)
    return { success: true }
  }

  function register(data: RegisterData): { success: boolean; message?: string } {
    const users = getStoredUsers()

    if (users.some(u => u.username === data.username)) {
      return { success: false, message: '用户名已被注册' }
    }
    if (users.some(u => u.email === data.email)) {
      return { success: false, message: '邮箱已被注册' }
    }

    const newUser: User = {
      id: `user-${Date.now()}`,
      username: data.username,
      email: data.email,
      role: 'user',
      password: data.password,
      avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${data.username}`,
      createdAt: new Date().toISOString(),
      lastActiveAt: new Date().toISOString()
    }

    users.push(newUser)
    saveUsers(users)
    currentUser.value = newUser
    persist(newUser)
    return { success: true }
  }
function logout() {
    currentUser.value = null
    persist(null)
  }

  function updateAvatar(avatarUrl: string) {
    if (!currentUser.value) return
    currentUser.value.avatar = avatarUrl
    persist(currentUser.value)

    const users = getStoredUsers()
    const idx = users.findIndex(u => u.id === currentUser.value!.id)
    if (idx !== -1) {
      users[idx].avatar = avatarUrl
      saveUsers(users)
    }
  }

  function changePassword(oldPassword: string, newPassword: string): { success: boolean; message?: string } {
    if (!currentUser.value) {
      return { success: false, message: '用户未登录' }
    }

    if (currentUser.value.password !== oldPassword) {
      return { success: false, message: '当前密码错误' }
    }

    currentUser.value.password = newPassword
    persist(currentUser.value)

    const users = getStoredUsers()
    const idx = users.findIndex(u => u.id === currentUser.value!.id)
    if (idx !== -1) {
      users[idx].password = newPassword
      saveUsers(users)
    }

    return { success: true }
  }

  // Demo helpers for quick role switching during development
  function setRole(role: UserRole) {
    if (currentUser.value) {
      currentUser.value.role = role
      persist(currentUser.value)
    }
  }

  return {
    currentUser,
    isLoggedIn,
    isAdmin,
    userRole,
    login,
    register,
    logout,
    updateAvatar,
    changePassword,
    updateLastActive,
    setRole
  }
})

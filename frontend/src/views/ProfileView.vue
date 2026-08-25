<template>
  <div class="max-w-4xl mx-auto">
    <!-- Page header -->
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">个人中心</h1>
      <p class="text-gray-500">管理你的账号信息、头像与密码</p>
    </div>

    <div class="space-y-6">
      <!-- Basic info card -->
      <section class="card p-5 sm:p-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-5">基本信息</h2>
        <div class="flex flex-col sm:flex-row gap-6 items-start">
          <div class="flex flex-col items-center gap-3">
            <div class="relative">
              <img
                v-if="auth.currentUser?.avatar"
                :src="auth.currentUser.avatar"
                alt="avatar"
                class="w-24 h-24 rounded-full object-cover bg-gray-100 border-4 border-white shadow-md"
              >
              <div
                v-else
                class="w-24 h-24 rounded-full bg-gray-100 flex items-center justify-center text-2xl font-bold text-gray-500 border-4 border-white shadow-md"
              >
                {{ auth.currentUser?.username?.[0]?.toUpperCase() ?? 'U' }}
              </div>
              <div
                v-if="avatarLoading"
                class="absolute inset-0 rounded-full bg-white/80 flex items-center justify-center"
              >
                <svg class="animate-spin w-6 h-6 text-xhs-red" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
              </div>
            </div>
            <input
              ref="avatarInput"
              type="file"
              accept="image/jpeg,image/png,image/webp,image/gif"
              class="hidden"
              @change="handleAvatarChange"
            >
            <button
              type="button"
              class="px-4 py-2 text-sm font-medium text-xhs-red bg-red-50 hover:bg-red-100 rounded-xl transition-colors"
              @click="avatarInput?.click()"
            >
              修改头像
            </button>
            <p
              v-if="avatarError"
              class="max-w-48 text-center text-xs text-red-600"
            >
              {{ avatarError }}
            </p>
          </div>

          <div class="flex-1 w-full">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="p-4 rounded-xl bg-gray-50">
                <p class="text-xs text-gray-500 mb-1">用户名</p>
                <p class="text-sm font-medium text-gray-900">{{ auth.currentUser?.username }}</p>
              </div>
              <div class="p-4 rounded-xl bg-gray-50">
                <p class="text-xs text-gray-500 mb-1">邮箱</p>
                <p class="text-sm font-medium text-gray-900">{{ auth.currentUser?.email }}</p>
              </div>
              <div class="p-4 rounded-xl bg-gray-50">
                <p class="text-xs text-gray-500 mb-1">角色</p>
                <p class="text-sm font-medium text-gray-900">{{ auth.isAdmin ? '管理员' : '普通用户' }}</p>
              </div>
              <div class="p-4 rounded-xl bg-gray-50">
                <p class="text-xs text-gray-500 mb-1">注册时间</p>
                <p class="text-sm font-medium text-gray-900">{{ formatDate(auth.currentUser?.createdAt) }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Password change card -->
      <section class="card p-5 sm:p-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-5">修改密码</h2>
        <form
          class="max-w-md space-y-4"
          @submit.prevent="handlePasswordSubmit"
        >
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">当前密码</label>
            <input
              v-model="passwordForm.oldPassword"
              type="password"
              placeholder="请输入当前密码"
              class="input"
            >
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">新密码</label>
            <input
              v-model="passwordForm.newPassword"
              type="password"
              placeholder="请输入新密码"
              class="input"
            >
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">确认新密码</label>
            <input
              v-model="passwordForm.confirmPassword"
              type="password"
              placeholder="请再次输入新密码"
              class="input"
            >
          </div>

          <div
            v-if="passwordMessage"
            class="rounded-xl px-4 py-3 text-sm flex items-start gap-2"
            :class="passwordSuccess ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'"
          >
            <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="passwordSuccess" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <span>{{ passwordMessage }}</span>
          </div>

          <button
            type="submit"
            class="btn-primary"
            :disabled="!canSubmitPassword"
          >
            保存密码
          </button>
        </form>
      </section>

      <!-- Account actions -->
      <section class="card p-5 sm:p-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-5">账号操作</h2>
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <p class="text-sm font-medium text-gray-900">退出登录</p>
            <p class="text-xs text-gray-500 mt-1">退出后将无法继续使用工作台功能</p>
          </div>
          <button
            type="button"
            class="px-5 py-2.5 text-sm font-medium text-white bg-xhs-red hover:bg-red-600 rounded-xl transition-colors flex items-center gap-2"
            @click="handleLogout"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            退出登录
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useHistoryStore } from '@/stores/history'
import { uploadImage } from '@/services/generationApi'

const router = useRouter()
const auth = useAuthStore()
const historyStore = useHistoryStore()

const avatarInput = ref<HTMLInputElement | null>(null)
const avatarLoading = ref(false)
const avatarError = ref('')

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const passwordMessage = ref('')
const passwordSuccess = ref(false)

const canSubmitPassword = computed(() =>
  passwordForm.oldPassword &&
  passwordForm.newPassword &&
  passwordForm.confirmPassword &&
  passwordForm.newPassword === passwordForm.confirmPassword
)

async function handleAvatarChange(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return

  avatarLoading.value = true
  avatarError.value = ''
  try {
    const uploaded = await uploadImage(file)
    await auth.updateAvatar(uploaded.url)
  } catch (error) {
    avatarError.value = error instanceof Error ? error.message : '头像上传失败'
  } finally {
    avatarLoading.value = false
    if (avatarInput.value) {
      avatarInput.value.value = ''
    }
  }
}

async function handlePasswordSubmit() {
  passwordMessage.value = ''

  if (passwordForm.newPassword.length < 6) {
    passwordMessage.value = '新密码长度不能少于 6 位'
    passwordSuccess.value = false
    return
  }

  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    passwordMessage.value = '两次输入的新密码不一致'
    passwordSuccess.value = false
    return
  }

  const result = await auth.changePassword(passwordForm.oldPassword, passwordForm.newPassword)
  if (result.success) {
    passwordMessage.value = '密码修改成功'
    passwordSuccess.value = true
    passwordForm.oldPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
  } else {
    passwordMessage.value = result.message || '密码修改失败'
    passwordSuccess.value = false
  }
}

async function handleLogout() {
  await auth.logout()
  historyStore.clearHistory()
  router.push('/login')
}

function formatDate(isoString?: string) {
  if (!isoString) return '-'
  const date = new Date(isoString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

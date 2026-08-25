<template>
  <AppLayout>
    <div class="min-h-[calc(100vh-8rem)] flex items-center justify-center px-4 py-12">
      <div class="w-full max-w-md">
        <div class="card p-8">
          <div class="text-center mb-8">
            <div class="w-12 h-12 rounded-xl bg-xhs-red flex items-center justify-center text-white font-bold text-xl mx-auto mb-4 shadow-lg shadow-red-200">
              红
            </div>
            <h1 class="text-2xl font-bold text-gray-900">创建账号</h1>
            <p class="text-sm text-gray-500 mt-2">注册后免费使用文案生成功能</p>
          </div>

          <form
            class="space-y-5"
            @submit.prevent="handleRegister"
          >
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">用户名</label>
              <input
                v-model="form.username"
                type="text"
                placeholder="设置用户名"
                class="input"
                required
              >
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
              <input
                v-model="form.email"
                type="email"
                placeholder="your@email.com"
                class="input"
                required
              >
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">密码</label>
              <input
                v-model="form.password"
                type="password"
                placeholder="设置密码"
                class="input"
                required
              >
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">确认密码</label>
              <input
                v-model="form.confirmPassword"
                type="password"
                placeholder="再次输入密码"
                class="input"
                required
              >
            </div>

            <div
              v-if="error"
              class="p-3 rounded-xl bg-red-50 text-red-600 text-sm"
            >
              {{ error }}
            </div>

            <button
              type="submit"
              class="btn-primary w-full py-3.5 text-base"
              :disabled="loading"
            >
              <svg
                v-if="loading"
                class="animate-spin -ml-1 mr-2 h-5 w-5 text-white"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              {{ loading ? '注册中...' : '注册' }}
            </button>
          </form>

          <div class="mt-6 text-center text-sm text-gray-500">
            已有账号？
            <RouterLink
              to="/login"
              class="text-xhs-red font-medium hover:text-red-700"
            >
              立即登录
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue'
import { useAuthStore } from '@/stores/auth'
import { useHistoryStore } from '@/stores/history'

const auth = useAuthStore()
const historyStore = useHistoryStore()
const router = useRouter()

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})
const loading = ref(false)
const error = ref('')

async function handleRegister() {
  error.value = ''

  if (form.password !== form.confirmPassword) {
    error.value = '两次输入的密码不一致'
    return
  }
  if (form.password.length < 6) {
    error.value = '密码长度至少为 6 位'
    return
  }

  loading.value = true
  const res = await auth.register({
    username: form.username.trim(),
    email: form.email.trim(),
    password: form.password
  })

  loading.value = false
  if (!res.success) {
    error.value = res.message || '注册失败'
    return
  }

  await historyStore.loadHistory()
  router.push('/workspace')
}
</script>

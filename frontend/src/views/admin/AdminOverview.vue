<template>
  <AdminLayout>
    <div class="space-y-6">
      <LoadingState
        v-if="loading"
        title="加载数据中"
        subtitle="正在获取后台概览数据..."
      />

      <template v-else-if="overview">
        <!-- Stats grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">
          <StatCard
            label="用户总数"
            :value="overview.totalUsers"
            :trend="12"
            type="users"
          />
          <StatCard
            label="累计生成次数"
            :value="overview.totalGenerations"
            :trend="8"
            type="generations"
          />
          <StatCard
            label="今日生成"
            :value="overview.todayGenerations"
            :trend="-3"
            type="today"
          />
          <StatCard
            label="生成成功率"
            :value="`${overview.successRate}%`"
            :trend="2"
            type="success"
          />
        </div>

        <!-- Chart -->
        <TrendChart :data="overview.dailyStats" />

        <!-- Extra metrics -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-card">
            <h3 class="text-lg font-bold text-gray-900 mb-4">模型性能</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-500">平均生成耗时</span>
                <span class="font-semibold text-gray-900">{{ (overview.avgGenerationTimeMs / 1000).toFixed(1) }}s</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-500">目标耗时</span>
                <span class="font-semibold text-gray-900">&lt; 15s</span>
              </div>
              <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                <div
                  class="h-full bg-xhs-red rounded-full"
                  :style="{ width: `${Math.min((overview.avgGenerationTimeMs / 15000) * 100, 100)}%` }"
                />
              </div>
            </div>
          </div>

          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-card">
            <h3 class="text-lg font-bold text-gray-900 mb-4">最近活跃</h3>
            <div class="space-y-3">
              <div
                v-for="user in recentUsers"
                :key="user.id"
                class="flex items-center justify-between"
              >
                <div class="flex items-center gap-3">
                  <img
                    v-if="user.avatar"
                    :src="user.avatar"
                    alt="avatar"
                    class="w-8 h-8 rounded-full bg-gray-100"
                  >
                  <div
                    v-else
                    class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-xs font-bold text-gray-500"
                  >
                    {{ user.username[0].toUpperCase() }}
                  </div>
                  <span class="text-sm font-medium text-gray-900">{{ user.username }}</span>
                </div>
                <span class="text-xs text-gray-400">{{ formatTime(user.lastActiveAt) }}</span>
              </div>
            </div>
          </div>
        </div>
      </template>

      <ErrorState
        v-else
        message="无法加载概览数据"
        show-retry
        @retry="load"
      />
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import StatCard from '@/components/admin/StatCard.vue'
import TrendChart from '@/components/admin/TrendChart.vue'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'
import { getAdminOverview, getUsers } from '@/services/adminApi'
import type { AdminOverview, User } from '@/types'

const overview = ref<AdminOverview | null>(null)
const users = ref<User[]>([])
const loading = ref(false)

const recentUsers = computed(() => {
  return [...users.value]
    .sort((a, b) => new Date(b.lastActiveAt).getTime() - new Date(a.lastActiveAt).getTime())
    .slice(0, 5)
})

async function load() {
  loading.value = true
  overview.value = null
  try {
    const [overviewData, usersData] = await Promise.all([
      getAdminOverview(),
      getUsers()
    ])
    overview.value = overviewData
    users.value = usersData
  } catch {
    overview.value = null
  } finally {
    loading.value = false
  }
}

function formatTime(isoString: string) {
  const date = new Date(isoString)
  return date.toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(load)
</script>

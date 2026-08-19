<template>
  <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-card">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h3 class="text-lg font-bold text-gray-900">每日生成趋势</h3>
        <p class="text-sm text-gray-500 mt-1">近 14 天文案生成量与成功率</p>
      </div>
      <div class="flex items-center gap-4 text-sm">
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-full bg-xhs-red" />
          <span class="text-gray-600">生成总数</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-full bg-green-500" />
          <span class="text-gray-600">成功数</span>
        </div>
      </div>
    </div>

    <div class="relative h-64 w-full">
      <svg
        class="w-full h-full"
        preserveAspectRatio="none"
        viewBox="0 0 100 100"
      >
        <!-- Grid lines -->
        <line
          x1="0"
          y1="25"
          x2="100"
          y2="25"
          stroke="#f3f4f6"
          stroke-width="0.5"
        />
        <line
          x1="0"
          y1="50"
          x2="100"
          y2="50"
          stroke="#f3f4f6"
          stroke-width="0.5"
        />
        <line
          x1="0"
          y1="75"
          x2="100"
          y2="75"
          stroke="#f3f4f6"
          stroke-width="0.5"
        />

        <!-- Total generations area -->
        <polygon
          :points="totalAreaPoints"
          fill="rgba(255, 36, 66, 0.1)"
        />
        <polyline
          :points="totalLinePoints"
          fill="none"
          stroke="#ff2442"
          stroke-width="1"
          stroke-linecap="round"
          stroke-linejoin="round"
        />

        <!-- Success count line -->
        <polyline
          :points="successLinePoints"
          fill="none"
          stroke="#22c55e"
          stroke-width="1"
          stroke-linecap="round"
          stroke-linejoin="round"
        />

        <!-- Data points -->
        <circle
          v-for="(point, index) in totalPoints"
          :key="`t-${index}`"
          :cx="point.x"
          :cy="point.y"
          r="1"
          fill="#ff2442"
        />
      </svg>

      <!-- X-axis labels -->
      <div class="absolute bottom-0 left-0 right-0 flex justify-between text-xs text-gray-400 px-2">
        <span
          v-for="(label, index) in xLabels"
          :key="index"
        >{{ label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { DailyStats } from '@/types'

interface Props {
  data: DailyStats[]
}

const props = defineProps<Props>()

const chartData = computed(() => props.data.slice(-14))

const maxValue = computed(() => {
  return Math.max(...chartData.value.map(d => d.totalGenerations), 1)
})

function getPoint(index: number, value: number) {
  const x = chartData.value.length <= 1 ? 50 : (index / (chartData.value.length - 1)) * 90 + 5
  const y = 95 - (value / maxValue.value) * 80
  return { x, y }
}

const totalPoints = computed(() => {
  return chartData.value.map((d, i) => getPoint(i, d.totalGenerations))
})

const successPoints = computed(() => {
  return chartData.value.map((d, i) => getPoint(i, d.successCount))
})

const totalLinePoints = computed(() => {
  return totalPoints.value.map(p => `${p.x},${p.y}`).join(' ')
})

const successLinePoints = computed(() => {
  return successPoints.value.map(p => `${p.x},${p.y}`).join(' ')
})

const totalAreaPoints = computed(() => {
  const first = totalPoints.value[0]
  const last = totalPoints.value[totalPoints.value.length - 1]
  return `${first.x},95 ${totalLinePoints.value} ${last.x},95`
})

const xLabels = computed(() => {
  const len = chartData.value.length
  if (len === 0) return []
  if (len <= 4) return chartData.value.map(d => d.date.slice(5))
  return [
    chartData.value[0].date.slice(5),
    chartData.value[Math.floor(len / 3)].date.slice(5),
    chartData.value[Math.floor(len * 2 / 3)].date.slice(5),
    chartData.value[len - 1].date.slice(5)
  ]
})
</script>

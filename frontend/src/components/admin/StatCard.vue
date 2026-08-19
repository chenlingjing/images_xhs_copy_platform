<template>
  <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-card">
    <div class="flex items-start justify-between">
      <div>
        <p class="text-sm font-medium text-gray-500">{{ label }}</p>
        <p class="text-2xl font-bold text-gray-900 mt-2">{{ value }}</p>
        <p
          v-if="trend !== undefined"
          class="text-xs mt-2"
          :class="trend >= 0 ? 'text-green-600' : 'text-red-500'"
        >
          {{ trend >= 0 ? '↑' : '↓' }} {{ Math.abs(trend) }}% 较上周
        </p>
      </div>
      <div
        class="w-10 h-10 rounded-xl flex items-center justify-center"
        :class="iconBgClass"
      >
        <svg
          class="w-5 h-5"
          :class="iconColorClass"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          v-html="iconSvg"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

type StatType = 'users' | 'generations' | 'today' | 'success'

interface Props {
  label: string
  value: string | number
  trend?: number
  type: StatType
}

const props = defineProps<Props>()

const config: Record<StatType, { bg: string; color: string; path: string }> = {
  users: {
    bg: 'bg-blue-50',
    color: 'text-blue-600',
    path: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />'
  },
  generations: {
    bg: 'bg-purple-50',
    color: 'text-purple-600',
    path: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />'
  },
  today: {
    bg: 'bg-orange-50',
    color: 'text-orange-600',
    path: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />'
  },
  success: {
    bg: 'bg-green-50',
    color: 'text-green-600',
    path: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />'
  }
}

const iconSvg = computed(() => config[props.type].path)
const iconBgClass = computed(() => config[props.type].bg)
const iconColorClass = computed(() => config[props.type].color)
</script>

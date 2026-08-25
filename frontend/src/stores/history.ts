import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import type { GenerationRecord } from '@/types'
import {
  deleteGenerationRecord,
  getGenerationRecords
} from '@/services/generationApi'
import { useAuthStore } from './auth'

export const useHistoryStore = defineStore('history', () => {
  const auth = useAuthStore()
  const records = ref<GenerationRecord[]>([])
  const loading = ref(false)

  const isEmpty = computed(() => records.value.length === 0)
  const sortedRecords = computed(() => {
    return [...records.value].sort(
      (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    )
  })

  async function loadHistory() {
    if (!auth.isLoggedIn) {
      records.value = []
      return
    }
    loading.value = true
    try {
      records.value = await getGenerationRecords()
    } catch {
      records.value = []
    } finally {
      loading.value = false
    }
  }

  function clearHistory() {
    records.value = []
  }

  async function deleteRecord(id: string) {
    await deleteGenerationRecord(id)
    records.value = records.value.filter(record => record.id !== id)
  }

  function findById(id: string) {
    return records.value.find(record => record.id === id)
  }

  return {
    records,
    loading,
    isEmpty,
    sortedRecords,
    loadHistory,
    clearHistory,
    deleteRecord,
    findById
  }
})

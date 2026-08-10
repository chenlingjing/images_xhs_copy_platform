import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { GenerationRecord } from '@/types'
import { useAuthStore } from './auth'

function getStorageKey(userId: string) {
  return `xhs_history_${userId}`
}

export const useHistoryStore = defineStore('history', () => {
  const auth = useAuthStore()
  const records = ref<GenerationRecord[]>([])

  const isEmpty = computed(() => records.value.length === 0)
  const sortedRecords = computed(() => {
    return [...records.value].sort(
      (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    )
  })

  function loadHistory(userId?: string) {
    const id = userId || auth.currentUser?.id
    if (!id) {
      records.value = []
      return
    }
    try {
      const saved = localStorage.getItem(getStorageKey(id))
      records.value = saved ? JSON.parse(saved) : []
    } catch {
      records.value = []
    }
  }

  function saveHistory(userId?: string) {
    const id = userId || auth.currentUser?.id
    if (!id) return
    localStorage.setItem(getStorageKey(id), JSON.stringify(records.value))
  }

  function clearHistory() {
    records.value = []
  }

  function addRecord(record: GenerationRecord, userId?: string) {
    records.value.unshift(record)
    saveHistory(userId)
  }

  function deleteRecord(id: string, userId?: string) {
    records.value = records.value.filter(r => r.id !== id)
    saveHistory(userId)
  }

  function findById(id: string) {
    return records.value.find(r => r.id === id)
  }

  return {
    records,
    isEmpty,
    sortedRecords,
    loadHistory,
    saveHistory,
    clearHistory,
    addRecord,
    deleteRecord,
    findById
  }
})

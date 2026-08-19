<template>
  <RouterView />
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useHistoryStore } from '@/stores/history'

const auth = useAuthStore()
const historyStore = useHistoryStore()

onMounted(() => {
  if (auth.isLoggedIn) {
    historyStore.loadHistory()
  }
})
</script>

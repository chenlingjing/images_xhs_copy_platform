<template>
  <div class="min-h-screen bg-xhs-bg flex flex-col overflow-x-hidden">
    <!-- Mobile header -->
    <header class="sticky top-0 z-40 bg-white/80 backdrop-blur-md border-b border-gray-100 lg:hidden">
      <div class="px-4 h-14 flex items-center justify-between">
        <RouterLink
          to="/"
          class="flex items-center gap-2"
        >
          <div class="w-8 h-8 rounded-lg bg-xhs-red flex items-center justify-center text-white font-bold text-sm">
            红
          </div>
          <span class="font-bold text-gray-900">小红书文案</span>
        </RouterLink>
        <button
          type="button"
          class="p-2 rounded-lg hover:bg-gray-100"
          aria-label="打开菜单"
          @click="drawerOpen = true"
        >
          <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
    </header>

    <div class="flex flex-1">
      <!-- Desktop sidebar (fixed, follows scroll) -->
      <aside class="hidden lg:flex fixed left-0 top-0 z-30 h-screen w-64 flex-col bg-white border-r border-gray-200 overflow-y-auto">
        <SidebarContent />
      </aside>

      <!-- Mobile drawer -->
      <Transition
        enter-active-class="transition-opacity duration-200"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-200"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="drawerOpen"
          class="fixed inset-0 z-50 lg:hidden"
        >
          <!-- Backdrop -->
          <div
            class="absolute inset-0 bg-black/40"
            @click="drawerOpen = false"
          />
          <!-- Drawer panel -->
          <div class="absolute left-0 top-0 bottom-0 w-64 bg-white shadow-2xl flex flex-col">
            <div class="h-14 flex items-center justify-between px-4 border-b border-gray-100">
              <span class="font-bold text-gray-900">菜单</span>
              <button
                type="button"
                class="p-2 rounded-lg hover:bg-gray-100"
                aria-label="关闭菜单"
                @click="drawerOpen = false"
              >
                <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <SidebarContent />
          </div>
        </div>
      </Transition>

      <!-- Main content -->
      <main class="flex-1 min-w-0 p-4 sm:p-6 lg:p-8 lg:ml-64">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import SidebarContent from './WorkspaceSidebarContent.vue'

const drawerOpen = ref(false)
</script>

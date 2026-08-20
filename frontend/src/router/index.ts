import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import WorkspaceLayout from '@/components/WorkspaceLayout.vue'
import WorkspaceView from '@/views/WorkspaceView.vue'
import HistoryView from '@/views/HistoryView.vue'
import ProfileView from '@/views/ProfileView.vue'
import AdminOverview from '@/views/admin/AdminOverview.vue'
import AdminUsers from '@/views/admin/AdminUsers.vue'
import AdminGenerations from '@/views/admin/AdminGenerations.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, _from, savedPosition) {
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0 }
  },
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { requiresGuest: true }
    },
    {
      path: '/workspace',
      component: WorkspaceLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          redirect: { name: 'generate' }
        },
        {
          path: 'generate',
          name: 'generate',
          component: WorkspaceView
        },
        {
          path: 'history',
          name: 'history',
          component: HistoryView
        },
        {
          path: 'profile',
          name: 'profile',
          component: ProfileView
        }
      ]
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminOverview,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/users',
      name: 'admin-users',
      component: AdminUsers,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/generations',
      name: 'admin-generations',
      component: AdminGenerations,
      meta: { requiresAuth: true, requiresAdmin: true }
    }
  ]
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }

  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return { path: '/workspace', query: { adminDenied: '1' } }
  }

  if (to.meta.requiresGuest && auth.isLoggedIn) {
    return { path: '/workspace' }
  }
})

export default router

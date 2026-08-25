import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from '@/stores/auth'
import './style.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)

async function bootstrap() {
  await useAuthStore(pinia).initialize()
  app.use(router)

  window.addEventListener('auth:unauthorized', () => {
    if (router.currentRoute.value.meta.requiresAuth) {
      router.push('/login')
    }
  })

  app.mount('#app')
}

void bootstrap()

import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/chat' },
    { path: '/chat', name: 'Chat', component: () => import('../views/Chat.vue'), meta: { title: 'Chat' } },
    { path: '/dashboard', name: 'Dashboard', component: () => import('../views/Dashboard.vue'), meta: { title: 'Dashboard' } },
  ],
})

router.afterEach((to) => {
  const title = (to.meta?.title as string) || 'Compatibilidade Conversacional'
  document.title = `${title} | Compatibilidade Conversacional com IA`
})

export default router

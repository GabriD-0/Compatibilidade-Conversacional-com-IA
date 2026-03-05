import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', name: 'Login', component: () => import('../views/Login.vue'), meta: { title: 'Login' } },
    // { path: '/home', name: 'Home', component: () => import('../views/Home.vue'), meta: { title: 'Home' } },
    // { path: '/chat', name: 'Chat', component: () => import('../views/Chat.vue'), meta: { title: 'Chat' } },
    // { path: '/dashboard', name: 'Dashboard', component: () => import('../views/Dashboard.vue'), meta: { title: 'Dashboard' } },
  ],
})

// TODO: Revisar o titulo da pagina
router.afterEach((to) => {
  const title = (to.meta?.title as string) || 'Compatibilidade Conversacional'
  document.title = `${title}`
})

export default router
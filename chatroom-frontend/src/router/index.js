import { createRouter, createWebHistory } from 'vue-router'
import AuthPage from '@/views/AuthPage.vue'
import { h } from 'vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'auth',
      component: AuthPage
    },

    {
      path: '/chat',
      name: 'chat',
      component: () => import('@/views/ChatPage.vue'),
      meta: {
        requiresAuth: true
      }
    },

    {
      path: '/update-user-info',
      name: 'updateUserInfo',
      component: () => import('@/views/UpdateUserInfoPage.vue'),
      meta: {
        requiresAuth: true
      }
    },

    {
      path: '/:catchAll(.*)*',
      name: 'NotFound',
      component: h(
        'p',
        {
          style:
            'color: red; display: flex; align-items: center; justify-content: center; font-size: 2rem;'
        },
        '404 Notfound'
      )
    }
  ]
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !localStorage.getItem('access') && !localStorage.getItem('id')) {
    return { name: 'auth' }
  }
})

export default router

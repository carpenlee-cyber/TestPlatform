import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import Login from '../views/Login.vue'
import MainLayout from '../layouts/MainLayout.vue'
import Dashboard from '../views/Dashboard.vue'
import TestCases from '../views/TestCases.vue'
import Bugs from '../views/Bugs.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { public: true }
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { title: '仪表盘' }
      },
      {
        path: 'test-cases',
        name: 'TestCases',
        component: TestCases,
        meta: { title: '测试用例' }
      },
      {
        path: 'bugs',
        name: 'Bugs',
        component: Bugs,
        meta: { title: 'Bug管理' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (!to.meta.public && !authStore.isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && authStore.isLoggedIn) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router

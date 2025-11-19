import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../views/MainLayout.vue'
import DashboardView from '../views/DashboardView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: MainLayout,
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

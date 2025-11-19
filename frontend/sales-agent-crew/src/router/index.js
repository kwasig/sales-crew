import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../views/MainLayout.vue'
import AnalyticsView from '../views/AnalyticsView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: MainLayout,
  },
  {
    path: '/analytics',
    name: 'analytics',
    component: AnalyticsView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

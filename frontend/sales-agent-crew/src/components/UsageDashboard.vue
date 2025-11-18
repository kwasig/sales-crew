<template>
  <div class="usage-dashboard border-t border-gray-200 pt-4 mt-4">
    <h3 class="text-lg font-semibold text-gray-900 mb-3">Usage Metrics</h3>
    
    <!-- Summary Cards -->
    <div class="grid grid-cols-2 gap-3 mb-4">
      <div class="bg-gray-50 p-3 rounded-lg border border-gray-200">
        <h4 class="text-xs font-medium text-gray-600">Total Searches</h4>
        <p class="text-lg font-bold text-gray-900">{{ metrics.totalSearches }}</p>
      </div>
      <div class="bg-gray-50 p-3 rounded-lg border border-gray-200">
        <h4 class="text-xs font-medium text-gray-600">Today</h4>
        <p class="text-lg font-bold text-gray-900">{{ metrics.searchesToday }}</p>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="bg-gray-50 p-3 rounded-lg border border-gray-200">
      <h4 class="text-sm font-medium text-gray-700 mb-2">Recent Activity</h4>
      <div class="space-y-2">
        <div 
          v-for="(activity, index) in recentActivity" 
          :key="index"
          class="text-xs text-gray-600 flex justify-between"
        >
          <span class="truncate">{{ activity.query }}</span>
          <span class="text-gray-500">{{ activity.time }}</span>
        </div>
        <div v-if="recentActivity.length === 0" class="text-xs text-gray-500 italic">
          No recent activity
        </div>
      </div>
    </div>

    <!-- Performance Metrics -->
    <div class="mt-3 bg-gray-50 p-3 rounded-lg border border-gray-200">
      <h4 class="text-sm font-medium text-gray-700 mb-2">Performance</h4>
      <div class="space-y-2 text-xs">
        <div class="flex justify-between">
          <span class="text-gray-600">Avg. Response</span>
          <span class="font-medium">{{ metrics.avgResponseTime }}s</span>
        </div>
        <div class="flex justify-between">
          <span class="text-gray-600">Success Rate</span>
          <span class="font-medium">{{ metrics.successRate }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useAuth } from '@clerk/vue'

const { userId } = useAuth()

const metrics = ref({
  totalSearches: 0,
  searchesToday: 0,
  avgResponseTime: 0,
  successRate: 100
})

const recentActivity = ref([])

// Load usage metrics from localStorage
const loadUsageMetrics = () => {
  try {
    const userMetrics = localStorage.getItem(`usage-metrics-${userId}`)
    if (userMetrics) {
      const parsed = JSON.parse(userMetrics)
      metrics.value = { ...metrics.value, ...parsed }
    }
  } catch (error) {
    console.error('Error loading usage metrics:', error)
  }
}

// Load recent activity from search history
const loadRecentActivity = () => {
  try {
    const userHistory = localStorage.getItem(`search-history-${userId}`)
    if (userHistory) {
      const history = JSON.parse(userHistory)
      recentActivity.value = history.slice(0, 3).map(search => ({
        query: search.query.length > 20 ? search.query.substring(0, 20) + '...' : search.query,
        time: new Date(search.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }))
    }
  } catch (error) {
    console.error('Error loading recent activity:', error)
  }
}

// Calculate metrics from search history
const calculateMetrics = () => {
  try {
    const userHistory = localStorage.getItem(`search-history-${userId}`)
    if (userHistory) {
      const history = JSON.parse(userHistory)
      const today = new Date().toDateString()
      
      metrics.value.totalSearches = history.length
      metrics.value.searchesToday = history.filter(search => 
        new Date(search.timestamp).toDateString() === today
      ).length
      
      // Calculate average response time (mock data for now)
      if (history.length > 0) {
        const totalTime = history.reduce((sum, search) => sum + (search.duration || 2.5), 0)
        metrics.value.avgResponseTime = (totalTime / history.length).toFixed(1)
      }
    }
  } catch (error) {
    console.error('Error calculating metrics:', error)
  }
}

// Initialize metrics
onMounted(() => {
  loadUsageMetrics()
  loadRecentActivity()
  calculateMetrics()
})

// Watch for changes in search history
watch(() => {
  // This watch will trigger when localStorage changes
  return localStorage.getItem(`search-history-${userId}`)
}, () => {
  loadRecentActivity()
  calculateMetrics()
})

// Expose methods for external updates
defineExpose({
  updateMetrics: () => {
    loadRecentActivity()
    calculateMetrics()
  }
})
</script>

<style scoped>
.usage-dashboard {
  font-size: 0.8rem;
}
</style>
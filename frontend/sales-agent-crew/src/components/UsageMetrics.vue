<template>
  <div class="bg-gray-50 border-t border-gray-200 p-4 mt-auto">
    <h3 class="text-sm font-semibold text-gray-900 mb-2">Usage Metrics</h3>
    
    <!-- Real-time Metrics -->
    <div class="space-y-2">
      <div class="flex justify-between items-center">
        <span class="text-xs text-gray-600">Active Agents</span>
        <span class="text-xs font-medium text-primary-600">{{ metrics.activeAgents }}</span>
      </div>
      
      <div class="flex justify-between items-center">
        <span class="text-xs text-gray-600">Total Searches</span>
        <span class="text-xs font-medium text-primary-600">{{ metrics.totalSearches }}</span>
      </div>
      
      <div class="flex justify-between items-center">
        <span class="text-xs text-gray-600">Companies Found</span>
        <span class="text-xs font-medium text-primary-600">{{ metrics.companiesFound }}</span>
      </div>
      
      <div class="flex justify-between items-center">
        <span class="text-xs text-gray-600">Avg. Response Time</span>
        <span class="text-xs font-medium text-primary-600">{{ metrics.avgResponseTime }}s</span>
      </div>
      
      <!-- API Status -->
      <div class="flex justify-between items-center">
        <span class="text-xs text-gray-600">API Status</span>
        <span 
          class="text-xs font-medium"
          :class="metrics.apiStatus === 'Connected' ? 'text-green-600' : 'text-red-600'"
        >
          {{ metrics.apiStatus }}
        </span>
      </div>
    </div>
    
    <!-- Progress Bar for Current Search -->
    <div v-if="metrics.currentSearchProgress > 0" class="mt-3">
      <div class="flex justify-between items-center mb-1">
        <span class="text-xs text-gray-600">Current Search</span>
        <span class="text-xs text-gray-500">{{ metrics.currentSearchProgress }}%</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-1">
        <div 
          class="bg-primary-600 h-1 rounded-full transition-all duration-300"
          :style="{ width: metrics.currentSearchProgress + '%' }"
        ></div>
      </div>
    </div>
    
    <!-- Last Search Info -->
    <div v-if="metrics.lastSearchTime" class="mt-3 pt-3 border-t border-gray-200">
      <div class="text-xs text-gray-500">
        Last search: {{ formatTimeAgo(metrics.lastSearchTime) }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuth } from '@clerk/vue'

const { userId } = useAuth()

// Default metrics structure
const metrics = ref({
  activeAgents: 0,
  totalSearches: 0,
  companiesFound: 0,
  avgResponseTime: 0,
  apiStatus: 'Checking...',
  currentSearchProgress: 0,
  lastSearchTime: null
})

// Format time ago for display
const formatTimeAgo = (timestamp) => {
  if (!timestamp) return 'Never'
  
  const now = Date.now()
  const diff = now - timestamp
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (days > 0) return `${days}d ago`
  if (hours > 0) return `${hours}h ago`
  if (minutes > 0) return `${minutes}m ago`
  return 'Just now'
}

// Load metrics from localStorage
const loadMetrics = () => {
  const userMetrics = localStorage.getItem(`usage-metrics-${userId}`)
  if (userMetrics) {
    const parsed = JSON.parse(userMetrics)
    metrics.value = { ...metrics.value, ...parsed }
  }
}

// Save metrics to localStorage
const saveMetrics = () => {
  localStorage.setItem(
    `usage-metrics-${userId}`,
    JSON.stringify(metrics.value)
  )
}

// Update metrics when a search is performed
export const updateMetrics = (searchData) => {
  // Increment total searches
  metrics.value.totalSearches += 1
  
  // Update companies found
  if (searchData.results && Array.isArray(searchData.results)) {
    metrics.value.companiesFound += searchData.results.length
  }
  
  // Update last search time
  metrics.value.lastSearchTime = Date.now()
  
  // Calculate average response time (simplified)
  if (searchData.executionTime) {
    const currentAvg = metrics.value.avgResponseTime
    const newTime = searchData.executionTime / 1000 // Convert to seconds
    
    // Simple moving average
    metrics.value.avgResponseTime = ((currentAvg * (metrics.value.totalSearches - 1)) + newTime) / metrics.value.totalSearches
  }
  
  saveMetrics()
}

// Simulate API status check
const checkApiStatus = async () => {
  try {
    // In a real implementation, this would ping the backend API
    metrics.value.apiStatus = 'Connected'
    metrics.value.activeAgents = 4 // Based on the number of agents in ResearchCrew
  } catch (error) {
    metrics.value.apiStatus = 'Disconnected'
    metrics.value.activeAgents = 0
  }
}

// Simulate search progress (for demo purposes)
let progressInterval = null
const simulateSearchProgress = () => {
  if (progressInterval) clearInterval(progressInterval)
  
  metrics.value.currentSearchProgress = 0
  progressInterval = setInterval(() => {
    if (metrics.value.currentSearchProgress < 100) {
      metrics.value.currentSearchProgress += 10
    } else {
      clearInterval(progressInterval)
      // Reset after completion
      setTimeout(() => {
        metrics.value.currentSearchProgress = 0
      }, 2000)
    }
  }, 500)
}

// Expose methods for external use
defineExpose({
  updateMetrics,
  simulateSearchProgress
})

onMounted(() => {
  loadMetrics()
  checkApiStatus()
  
  // Check API status periodically
  const statusInterval = setInterval(checkApiStatus, 30000) // Every 30 seconds
  
  onUnmounted(() => {
    clearInterval(statusInterval)
    if (progressInterval) clearInterval(progressInterval)
  })
})
</script>

<style scoped>
/* Additional styling can be added here if needed */
</style>
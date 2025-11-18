<template>
  <div class="bg-white rounded-lg border border-gray-200 p-4 mt-4">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-gray-900">Agent Usage Dashboard</h3>
      <div class="flex items-center space-x-2">
        <span class="text-xs text-gray-500">Last updated: {{ lastUpdated }}</span>
        <button 
          @click="refreshMetrics"
          class="p-1 text-gray-400 hover:text-gray-600"
          :class="{ 'animate-spin': refreshing }"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.346 0A5.5 5.5 0 007 10.5V12m0 0v5.5a5.5 5.5 0 0010 0V12a5.5 5.5 0 00-10 0z" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-2 gap-4 mb-4">
      <div class="bg-blue-50 border border-blue-100 rounded-lg p-3">
        <div class="text-xs text-blue-600 font-medium">Total Searches</div>
        <div class="text-2xl font-bold text-blue-900">{{ formatNumber(metrics.total_searches) }}</div>
      </div>
      <div class="bg-green-50 border border-green-100 rounded-lg p-3">
        <div class="text-xs text-green-600 font-medium">Today's Usage</div>
        <div class="text-2xl font-bold text-green-900">{{ formatNumber(metrics.today_usage) }}</div>
      </div>
    </div>

    <!-- Performance Stats -->
    <div class="grid grid-cols-2 gap-4 mb-4">
      <div class="bg-purple-50 border border-purple-100 rounded-lg p-3">
        <div class="text-xs text-purple-600 font-medium">Avg. Response Time</div>
        <div class="text-lg font-semibold text-purple-900">{{ metrics.performance_stats.average_response_time.toFixed(2) }}s</div>
      </div>
      <div class="bg-yellow-50 border border-yellow-100 rounded-lg p-3">
        <div class="text-xs text-yellow-600 font-medium">Success Rate</div>
        <div class="text-lg font-semibold text-yellow-900">{{ metrics.performance_stats.success_rate.toFixed(1) }}%</div>
      </div>
    </div>

    <!-- Agent Usage -->
    <div class="mb-4">
      <h4 class="text-sm font-medium text-gray-700 mb-2">Agent Usage</h4>
      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <span class="text-sm text-gray-600">Lead Generation</span>
          <span class="font-medium">{{ formatNumber(metrics.agent_usage.lead_generation) }}</span>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-sm text-gray-600">Financial Analysis</span>
          <span class="font-medium">{{ formatNumber(metrics.agent_usage.financial_analysis) }}</span>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div>
      <h4 class="text-sm font-medium text-gray-700 mb-2">Recent Activity</h4>
      <div class="space-y-2 max-h-32 overflow-y-auto">
        <div 
          v-for="activity in metrics.recent_activity" 
          :key="activity.id"
          class="text-xs text-gray-500 border-l-2 border-gray-200 pl-2 py-1"
        >
          <div class="flex justify-between">
            <span class="font-medium">{{ activity.action }}</span>
            <span>{{ formatTime(activity.timestamp) }}</span>
          </div>
          <div class="text-gray-400">{{ activity.user_id }}</div>
        </div>
        <div v-if="metrics.recent_activity.length === 0" class="text-xs text-gray-400 italic">
          No recent activity
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuth } from '@clerk/vue'

const { userId } = useAuth()
const metrics = ref({
  total_searches: 0,
  today_usage: 0,
  recent_activity: [],
  performance_stats: {
    average_response_time: 0,
    success_rate: 100,
    total_errors: 0
  },
  agent_usage: {
    lead_generation: 0,
    financial_analysis: 0
  }
})
const lastUpdated = ref('')
const refreshing = ref(false)

const formatNumber = (num) => {
  return new Intl.NumberFormat().format(num)
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

const refreshMetrics = async () => {
  refreshing.value = true
  try {
    const response = await fetch('http://localhost:8001/usage-metrics')
    if (response.ok) {
      const data = await response.json()
      metrics.value = data
      lastUpdated.value = new Date().toLocaleTimeString()
    }
  } catch (error) {
    console.error('Failed to fetch metrics:', error)
  }
  refreshing.value = false
}

// Auto-refresh every 30 seconds
onMounted(() => {
  refreshMetrics()
  setInterval(refreshMetrics, 30000)
})
</script>
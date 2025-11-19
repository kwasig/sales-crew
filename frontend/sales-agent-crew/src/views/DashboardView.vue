<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Usage Dashboard</h1>
        <p class="text-gray-600 mt-2">Monitor system performance and user activity</p>
      </div>
      
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
        <p class="mt-4 text-gray-600">Loading dashboard data...</p>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 mb-6">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
          <h3 class="text-lg font-medium text-red-800">Error Loading Dashboard</h3>
        </div>
        <p class="mt-2 text-red-700">{{ error }}</p>
        <button @click="fetchDashboardData" class="mt-4 bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700">
          Retry
        </button>
      </div>
      
      <!-- Dashboard Content -->
      <div v-else class="space-y-6">
        <!-- System Health Overview -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white rounded-lg shadow-md p-6">
            <div class="flex items-center">
              <div class="p-2 rounded-full bg-green-100">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">System Status</p>
                <p class="text-2xl font-bold text-gray-900">{{ systemHealth.status || 'Unknown' }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-md p-6">
            <div class="flex items-center">
              <div class="p-2 rounded-full bg-blue-100">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Error Rate</p>
                <p class="text-2xl font-bold text-gray-900">{{ systemHealth.error_rate_percentage || 0 }}%</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-md p-6">
            <div class="flex items-center">
              <div class="p-2 rounded-full bg-purple-100">
                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Avg Response Time</p>
                <p class="text-2xl font-bold text-gray-900">{{ systemHealth.average_response_time_ms || 0 }}ms</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-md p-6">
            <div class="flex items-center">
              <div class="p-2 rounded-full bg-yellow-100">
                <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Uptime</p>
                <p class="text-2xl font-bold text-gray-900">{{ systemHealth.uptime_percentage || 0 }}%</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Usage Statistics -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- API Usage -->
          <div class="bg-white rounded-lg shadow-md p-6">
            <h3 class="text-lg font-semibold mb-4">API Usage</h3>
            <div class="space-y-3">
              <div v-for="(count, endpoint) in usageSummary.api_usage" :key="endpoint" 
                   class="flex justify-between items-center">
                <span class="text-sm text-gray-600 truncate">{{ endpoint }}</span>
                <span class="font-medium text-gray-900">{{ count }}</span>
              </div>
            </div>
          </div>
          
          <!-- Popular Searches -->
          <div class="bg-white rounded-lg shadow-md p-6">
            <h3 class="text-lg font-semibold mb-4">Popular Searches</h3>
            <div class="space-y-2">
              <div v-for="search in popularSearches" :key="search.query" 
                   class="flex justify-between items-center">
                <span class="text-sm text-gray-600 truncate">{{ search.query }}</span>
                <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                  {{ search.count }}
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Daily Analytics -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h3 class="text-lg font-semibold mb-4">Daily Activity (Last 7 Days)</h3>
          <div class="grid grid-cols-1 md:grid-cols-7 gap-4">
            <div v-for="day in dailyAnalytics" :key="day.date" 
                 class="text-center p-3 border rounded-lg">
              <p class="text-sm font-medium text-gray-600">{{ day.date }}</p>
              <p class="text-lg font-bold text-blue-600">{{ day.api_calls }}</p>
              <p class="text-xs text-gray-500">API Calls</p>
              <p class="text-sm text-green-600">{{ day.searches }}</p>
              <p class="text-xs text-gray-500">Searches</p>
              <p class="text-sm text-red-600">{{ day.errors }}</p>
              <p class="text-xs text-gray-500">Errors</p>
            </div>
          </div>
        </div>
        
        <!-- Performance Metrics -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h3 class="text-lg font-semibold mb-4">Performance Metrics</h3>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead>
                <tr>
                  <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Endpoint</th>
                  <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Calls</th>
                  <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Avg Time (ms)</th>
                  <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Max Time (ms)</th>
                  <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Min Time (ms)</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr v-for="(metrics, endpoint) in performanceMetrics" :key="endpoint">
                  <td class="px-4 py-2 text-sm text-gray-900">{{ endpoint }}</td>
                  <td class="px-4 py-2 text-sm text-gray-600">{{ metrics.call_count }}</td>
                  <td class="px-4 py-2 text-sm text-gray-600">{{ metrics.average_duration.toFixed(2) }}</td>
                  <td class="px-4 py-2 text-sm text-gray-600">{{ metrics.max_duration.toFixed(2) }}</td>
                  <td class="px-4 py-2 text-sm text-gray-600">{{ metrics.min_duration.toFixed(2) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getUsageSummary, getSystemHealth, getPopularSearches, getDailyAnalytics } from '../services/api.js'

export default {
  name: 'DashboardView',
  data() {
    return {
      loading: true,
      error: null,
      usageSummary: {},
      systemHealth: {},
      popularSearches: [],
      dailyAnalytics: [],
      performanceMetrics: {}
    }
  },
  async mounted() {
    await this.fetchDashboardData()
  },
  methods: {
    async fetchDashboardData() {
      this.loading = true
      this.error = null
      
      try {
        const [summaryResponse, healthResponse, searchesResponse, analyticsResponse] = await Promise.all([
          getUsageSummary(),
          getSystemHealth(),
          getPopularSearches(10),
          getDailyAnalytics()
        ])
        
        this.usageSummary = summaryResponse.data || {}
        this.systemHealth = healthResponse.data || {}
        this.popularSearches = searchesResponse.data?.popular_searches || []
        this.dailyAnalytics = analyticsResponse.data?.analytics || []
        this.performanceMetrics = this.usageSummary.performance_metrics || {}
        
      } catch (error) {
        this.error = error.response?.data?.error || error.message || 'Failed to load dashboard data'
        console.error('Dashboard error:', error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
/* Component-specific styles */
</style>
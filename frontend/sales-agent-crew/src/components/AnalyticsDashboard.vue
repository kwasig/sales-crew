<template>
  <div class="analytics-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <h1 class="text-2xl font-bold text-gray-900">Usage Analytics</h1>
      <p class="text-gray-600">Track your search activity and system usage</p>
    </div>

    <!-- Date Range Selector -->
    <div class="date-range-selector">
      <div class="flex items-center space-x-4">
        <div>
          <label for="start-date" class="block text-sm font-medium text-gray-700">Start Date</label>
          <input 
            type="date" 
            id="start-date" 
            v-model="startDate" 
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
          />
        </div>
        <div>
          <label for="end-date" class="block text-sm font-medium text-gray-700">End Date</label>
          <input 
            type="date" 
            id="end-date" 
            v-model="endDate" 
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
          />
        </div>
        <button 
          @click="fetchAnalytics" 
          :disabled="loading"
          class="mt-6 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:bg-gray-400"
        >
          {{ loading ? 'Loading...' : 'Update Analytics' }}
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="flex items-center justify-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <span class="ml-2 text-gray-600">Loading analytics data...</span>
      </div>
    </div>

    <!-- Analytics Content -->
    <div v-else-if="analyticsData" class="analytics-content">
      <!-- Summary Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="summary-card bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Total Searches</h3>
          <p class="text-3xl font-bold text-primary-600">{{ analyticsData.total_searches }}</p>
        </div>
        
        <div class="summary-card bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Successful Searches</h3>
          <p class="text-3xl font-bold text-green-600">{{ analyticsData.successful_searches }}</p>
        </div>
        
        <div class="summary-card bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Failed Searches</h3>
          <p class="text-3xl font-bold text-red-600">{{ analyticsData.failed_searches }}</p>
        </div>
        
        <div class="summary-card bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Total Results</h3>
          <p class="text-3xl font-bold text-blue-600">{{ analyticsData.total_results }}</p>
        </div>
      </div>

      <!-- API Usage -->
      <div class="api-usage-section bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-8">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">API Usage</h3>
        <div class="space-y-3">
          <div v-for="(count, api) in analyticsData.api_usage" :key="api" class="api-usage-item">
            <div class="flex justify-between items-center">
              <span class="text-gray-700">{{ formatApiName(api) }}</span>
              <span class="font-semibold text-primary-600">{{ count }}</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2 mt-1">
              <div 
                class="bg-primary-600 h-2 rounded-full" 
                :style="{ width: calculatePercentage(count, analyticsData.total_searches) + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- User Activity -->
      <div class="user-activity-section bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">User Activity</h3>
        <div class="space-y-3">
          <div v-for="(count, user) in analyticsData.user_activity" :key="user" class="user-activity-item">
            <div class="flex justify-between items-center">
              <span class="text-gray-700">{{ formatUserId(user) }}</span>
              <span class="font-semibold text-primary-600">{{ count }} searches</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2 mt-1">
              <div 
                class="bg-green-600 h-2 rounded-full" 
                :style="{ width: calculatePercentage(count, analyticsData.total_searches) + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Daily Averages -->
      <div v-if="analyticsData.daily_average" class="daily-averages-section bg-white p-6 rounded-lg shadow-sm border border-gray-200 mt-8">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Daily Averages</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 class="text-sm font-medium text-gray-500">Average Searches per Day</h4>
            <p class="text-2xl font-bold text-primary-600">{{ Math.round(analyticsData.daily_average.searches) }}</p>
          </div>
          <div>
            <h4 class="text-sm font-medium text-gray-500">Average Results per Day</h4>
            <p class="text-2xl font-bold text-blue-600">{{ Math.round(analyticsData.daily_average.results) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="error-state bg-red-50 border border-red-200 rounded-md p-4 mt-4">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">Error loading analytics</h3>
          <div class="mt-2 text-sm text-red-700">
            <p>{{ error }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAnalytics } from '../services/analytics'

const loading = ref(false)
const error = ref('')
const analyticsData = ref(null)

// Default to last 7 days
const startDate = ref(new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0])
const endDate = ref(new Date().toISOString().split('T')[0])

const fetchAnalytics = async () => {
  loading.value = true
  error.value = ''
  
  try {
    analyticsData.value = await getAnalytics(startDate.value, endDate.value)
  } catch (err) {
    error.value = err.message || 'Failed to fetch analytics data'
    console.error('Analytics error:', err)
  } finally {
    loading.value = false
  }
}

const formatApiName = (api) => {
  const names = {
    'sambanova': 'SambaNova AI',
    'exa': 'Exa Search',
    'openai': 'OpenAI'
  }
  return names[api] || api
}

const formatUserId = (userId) => {
  // Truncate user ID for display
  return userId.substring(0, 8) + '...'
}

const calculatePercentage = (value, total) => {
  if (total === 0) return 0
  return Math.round((value / total) * 100)
}

onMounted(() => {
  fetchAnalytics()
})
</script>

<style scoped>
.analytics-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.date-range-selector {
  margin-bottom: 2rem;
}

.summary-card {
  text-align: center;
}

.api-usage-item,
.user-activity-item {
  padding: 0.5rem 0;
}
</style>
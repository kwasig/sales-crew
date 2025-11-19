<template>
  <div class="relative flex h-screen">
    <!-- Collapse Button -->
    <button 
      @click="isCollapsed = !isCollapsed"
      class="absolute -right-3 top-4 z-20 bg-white rounded-full p-1 shadow-md border border-gray-200"
    >
      <svg 
        class="w-4 h-4 text-gray-600 transform transition-transform"
        :class="{ 'rotate-180': isCollapsed }"
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>

    <!-- Sidebar Content -->
    <div 
      class="bg-white border-r border-gray-200 flex flex-col transition-all duration-300 h-full"
      :class="{ 'w-64': !isCollapsed, 'w-0': isCollapsed }"
    >
      <!-- Fixed Header with Actions -->
      <div class="p-4 border-b border-gray-200 flex-shrink-0" v-show="!isCollapsed">
        <div class="flex justify-between items-center mb-2">
          <h2 class="text-lg font-semibold text-gray-900">Search History</h2>
          <div class="flex space-x-2">
            <button
              @click="exportAllChats"
              class="text-gray-600 hover:text-gray-900"
              title="Export All"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </button>
            <button
              @click="confirmClearAll"
              class="text-gray-600 hover:text-red-600"
              title="Clear All"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Scrollable History -->
      <div 
        class="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-transparent hover:scrollbar-thumb-gray-400"
        v-show="!isCollapsed"
      >
        <div class="p-4 space-y-3">
          <div
            v-for="(search, index) in searchHistory"
            :key="index"
            class="group relative bg-gray-50 rounded-lg p-3 hover:bg-gray-100 transition-colors"
          >
            <!-- Search Content -->
            <div class="pr-8">
              <div 
                class="text-sm font-medium text-gray-900 break-words"
                style="word-break: break-word;"
              >
                {{ search.query }}
              </div>
              <div class="text-xs text-gray-500 mt-1">
                {{ new Date(search.timestamp).toLocaleString() }}
              </div>
            </div>

            <!-- Actions (Only visible on hover) -->
            <div class="absolute top-2 right-2 flex space-x-1 opacity-0 group-hover:opacity-100 transition-opacity z-10">
              <button
                @click.stop="exportSearch(search)"
                class="p-1 text-gray-400 hover:text-gray-600"
                title="Export"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
              </button>
              <button
                @click.stop="deleteSearch(index)"
                class="p-1 text-gray-400 hover:text-red-600"
                title="Delete"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- Clickable Area for Loading Search -->
            <div 
              class="absolute inset-0 cursor-pointer z-0"
              @click="loadSearch(search)"
            ></div>
          </div>
        </div>

        <!-- Usage Dashboard Component -->
        <div class="p-4 border-t border-gray-200" v-show="!isCollapsed">
          <div class="bg-blue-50 rounded-lg p-4">
            <h3 class="text-sm font-semibold text-blue-900 mb-3">Agent Usage Dashboard</h3>
            
            <!-- Agent Metrics -->
            <div class="grid grid-cols-2 gap-3 mb-3">
              <div class="text-center">
                <div class="text-lg font-bold text-blue-700">{{ totalSearches }}</div>
                <div class="text-xs text-blue-600">Total Searches</div>
              </div>
              <div class="text-center">
                <div class="text-lg font-bold text-green-700">{{ todaysUsage }}</div>
                <div class="text-xs text-green-600">Today's Usage</div>
              </div>
            </div>

            <!-- Agent Type Breakdown -->
            <div class="space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-xs text-gray-600">Lead Generation</span>
                <span class="text-xs font-medium text-gray-800">{{ leadGenerationCount }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-xs text-gray-600">Financial Analysis</span>
                <span class="text-xs font-medium text-gray-800">{{ financialAnalysisCount }}</span>
              </div>
            </div>

            <!-- Performance Stats -->
            <div class="mt-3 pt-3 border-t border-blue-200">
              <div class="flex justify-between items-center text-xs">
                <span class="text-gray-600">Avg. Response Time</span>
                <span class="font-medium text-gray-800">{{ averageResponseTime }}s</span>
              </div>
              <div class="flex justify-between items-center text-xs mt-1">
                <span class="text-gray-600">Success Rate</span>
                <span class="font-medium text-gray-800">{{ successRate }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <div v-if="showConfirmModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white rounded-lg p-6 max-w-sm mx-4">
        <h3 class="text-lg font-semibold text-gray-900 mb-2">Clear All History?</h3>
        <p class="text-gray-600 mb-4">This action cannot be undone. Are you sure you want to clear all search history?</p>
        <div class="flex justify-end space-x-3">
          <button
            @click="showConfirmModal = false"
            class="px-4 py-2 text-gray-600 hover:text-gray-800"
          >
            Cancel
          </button>
          <button
            @click="clearAllHistory"
            class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Clear All
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuth } from '@clerk/vue'

const { userId } = useAuth()
const searchHistory = ref([])
const isCollapsed = ref(false)
const showConfirmModal = ref(false)

// Usage dashboard metrics
const totalSearches = computed(() => searchHistory.value.length)
const todaysUsage = computed(() => {
  const today = new Date().toDateString()
  return searchHistory.value.filter(search => 
    new Date(search.timestamp).toDateString() === today
  ).length
})

const leadGenerationCount = computed(() => {
  return searchHistory.value.filter(search => 
    search.query?.toLowerCase().includes('lead') || 
    search.query?.toLowerCase().includes('sales') ||
    search.results?.some(result => result.type === 'lead')
  ).length
})

const financialAnalysisCount = computed(() => {
  return searchHistory.value.filter(search => 
    search.query?.toLowerCase().includes('financial') || 
    search.query?.toLowerCase().includes('analysis') ||
    search.query?.toLowerCase().includes('news') ||
    search.results?.some(result => result.type === 'financial')
  ).length
})

const averageResponseTime = computed(() => {
  if (searchHistory.value.length === 0) return 0
  // Mock response time calculation - in real implementation, this would come from backend
  const totalTime = searchHistory.value.reduce((sum, search) => {
    return sum + (search.responseTime || Math.random() * 5 + 2) // Default 2-7 seconds
  }, 0)
  return (totalTime / searchHistory.value.length).toFixed(1)
})

const successRate = computed(() => {
  if (searchHistory.value.length === 0) return 0
  // Mock success rate - in real implementation, this would come from backend
  const successfulSearches = searchHistory.value.filter(search => 
    search.success !== false // Assume all are successful unless marked otherwise
  ).length
  return Math.round((successfulSearches / searchHistory.value.length) * 100)
})

const loadSearch = (search) => {
  emit('loadSearch', search)
}

// Load history from localStorage
onMounted(() => {
  const userHistory = localStorage.getItem(`search-history-${userId}`)
  if (userHistory) {
    searchHistory.value = JSON.parse(userHistory)
  }
})

// Delete single search
const deleteSearch = (index) => {
  searchHistory.value.splice(index, 1)
  saveHistory()
}

// Clear all history with confirmation
const confirmClearAll = () => {
  showConfirmModal.value = true
}

const clearAllHistory = () => {
  searchHistory.value = []
  saveHistory()
  showConfirmModal.value = false
}

// Export functions
const exportSearch = (search) => {
  const blob = new Blob([JSON.stringify(search, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `search-${new Date(search.timestamp).toISOString()}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const exportAllChats = () => {
  const blob = new Blob([JSON.stringify(searchHistory.value, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `all-searches-${new Date().toISOString()}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

// Save history to localStorage
const saveHistory = () => {
  localStorage.setItem(
    `search-history-${userId}`, 
    JSON.stringify(searchHistory.value)
  )
}

const emit = defineEmits(['loadSearch'])

// Expose method to add new searches
defineExpose({
  addSearch: (query, results, expandedState, type = null) => {
    const newSearch = {
      query,
      results,
      expandedState,
      timestamp: Date.now(),
      type: type || (query.toLowerCase().includes('financial') || query.toLowerCase().includes('analysis') ? 'financial' : 'lead'),
      responseTime: Math.random() * 5 + 2, // Mock response time for demo
      success: true // Assume success unless specified
    }
    searchHistory.value.unshift(newSearch)
    searchHistory.value = searchHistory.value.slice(0, 50) // Keep only last 50 searches
    saveHistory()
  }
})
</script> 
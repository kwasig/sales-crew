<script setup>
import { ref } from 'vue'
import { useAuth } from '@clerk/vue'
import Header from '../components/Header.vue'
import SearchSection from '../components/SearchSection.vue'
import SettingsModal from '../components/SettingsModal.vue'
import CompanyResultCard from '../components/CompanyResultCard.vue'
import SearchNotification from '../components/SearchNotification.vue'
import Sidebar from '../components/Sidebar.vue'

const settingsModalRef = ref(null)
const sidebarRef = ref(null)
const isLoading = ref(false)
const results = ref([])
const showNotification = ref(false)
const searchTime = ref(0)

const handleSearch = async (query) => {
  isLoading.value = true
  const startTime = Date.now()

  try {
    // Load API keys
    const { userId } = useAuth()
    const encryptedSambanovaKey = localStorage.getItem(`sambanova_key_${userId}`)
    const encryptedExaKey = localStorage.getItem(`exa_key_${userId}`)
    
    if (!encryptedSambanovaKey || !encryptedExaKey) {
      throw new Error('API keys not found. Please set them in settings.')
    }

    // Decrypt keys (assuming decryptKey function exists)
    const { decryptKey } = await import('../utils/encryption')
    const sambanovaKey = await decryptKey(encryptedSambanovaKey)
    const exaKey = await decryptKey(encryptedExaKey)

    // Perform actual search
    const { generateLeads } = await import('../services/api')
    const searchResult = await generateLeads(query, { sambanovaKey, exaKey })
    
    results.value = searchResult.outreach_list || []
    
    // Calculate search time
    const endTime = Date.now()
    searchTime.value = ((endTime - startTime) / 1000).toFixed(2)

    // Update sidebar with search history and usage metrics
    if (sidebarRef.value) {
      sidebarRef.value.addSearch(query, results.value, {}, searchResult.usage_metrics)
    }

    // Show notification
    showNotification.value = true
    setTimeout(() => {
      showNotification.value = false
    }, 5000)
  } catch (error) {
    console.error('Search error:', error)
    // Handle error (show notification, etc.)
  } finally {
    isLoading.value = false
  }
}

const openSettingsModal = () => {
  settingsModalRef.value.isOpen = true
}

const loadSearchFromHistory = (search) => {
  results.value = search.results || []
  searchTime.value = search.usage_metrics?.execution_time || 0
  
  // Update sidebar with current usage metrics
  if (sidebarRef.value && search.usage_metrics) {
    sidebarRef.value.updateUsageMetrics(search.usage_metrics)
  }
}
</script>

<template>
  <div class="h-screen flex">
    <!-- Sidebar -->
    <Sidebar ref="sidebarRef" @loadSearch="loadSearchFromHistory" />
    
    <!-- Main Content -->
    <div class="flex-1 flex flex-col">
      <Header />
      <main class="flex-1 p-6 overflow-y-auto">
        <SearchSection
          @search="handleSearch"
          @openSettings="openSettingsModal"
          :isLoading="isLoading"
        />

        <!-- Search Notification -->
        <SearchNotification 
          v-if="showNotification" 
          :show="showNotification" 
          :time="searchTime" 
          :resultCount="results.length" 
        />

        <!-- Results -->
        <div v-if="results.length > 0" class="space-y-4">
          <CompanyResultCard
            v-for="(company, index) in results"
            :key="index"
            :company="company"
          />
        </div>
      </main>

      <!-- Settings Modal -->
      <SettingsModal ref="settingsModalRef" />
    </div>
  </div>
</template>

<template>
  <div class="p-4 border-t border-gray-200 bg-gray-50">
    <h3 class="text-sm font-semibold text-gray-700 mb-3 flex items-center">
      <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
      Usage Metrics
    </h3>
    
    <div class="space-y-2">
      <div class="flex justify-between items-center text-xs">
        <span class="text-gray-500">Total Tokens</span>
        <span class="font-medium text-gray-900">{{ formatNumber(metrics.total_tokens) }}</span>
      </div>
      <div class="flex justify-between items-center text-xs">
        <span class="text-gray-500">Prompt Tokens</span>
        <span class="font-medium text-gray-900">{{ formatNumber(metrics.prompt_tokens) }}</span>
      </div>
      <div class="flex justify-between items-center text-xs">
        <span class="text-gray-500">Completion Tokens</span>
        <span class="font-medium text-gray-900">{{ formatNumber(metrics.completion_tokens) }}</span>
      </div>
      <div class="flex justify-between items-center text-xs">
        <span class="text-gray-500">Successful Requests</span>
        <span class="font-medium text-gray-900">{{ formatNumber(metrics.successful_requests) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  metrics: {
    type: Object,
    default: () => ({
      total_tokens: 0,
      prompt_tokens: 0,
      completion_tokens: 0,
      successful_requests: 0
    })
  }
})

const formatNumber = (num) => {
  return new Intl.NumberFormat('en-US').format(num || 0)
}
</script>

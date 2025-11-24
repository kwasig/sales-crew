<template>
  <div class="p-4 border-t border-gray-200 bg-gray-50">
    <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
      Agent Usage Stats
    </h3>
    
    <div v-if="usage" class="space-y-2">
      <div class="flex justify-between items-center text-sm">
        <span class="text-gray-600">Total Tokens:</span>
        <span class="font-medium text-gray-900">{{ usage.total_tokens || 0 }}</span>
      </div>
      
      <div class="flex justify-between items-center text-sm">
        <span class="text-gray-600">Prompt Tokens:</span>
        <span class="font-medium text-gray-900">{{ usage.prompt_tokens || 0 }}</span>
      </div>
      
      <div class="flex justify-between items-center text-sm">
        <span class="text-gray-600">Completion Tokens:</span>
        <span class="font-medium text-gray-900">{{ usage.completion_tokens || 0 }}</span>
      </div>
      
      <div class="flex justify-between items-center text-sm">
        <span class="text-gray-600">Successful Requests:</span>
        <span class="font-medium text-gray-900">{{ usage.successful_requests || 0 }}</span>
      </div>
    </div>
    
    <div v-else class="text-sm text-gray-400 italic text-center py-2">
      No usage data available
    </div>
  </div>
</template>

<script setup>
defineProps({
  usage: {
    type: Object,
    default: null
  }
})
</script>
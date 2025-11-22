<template>
  <div class="p-4 border-t border-gray-200 bg-gray-50">
    <h3 class="text-sm font-semibold text-gray-700 mb-3">Usage Metrics</h3>
    <div class="space-y-2">
      <div class="flex justify-between items-center">
        <span class="text-sm text-gray-600">Agents Used</span>
        <span class="text-sm font-medium text-gray-900">{{ agentCount }}</span>
      </div>
      <div class="flex justify-between items-center">
        <span class="text-sm text-gray-600">Execution Time</span>
        <span class="text-sm font-medium text-gray-900">{{ formattedTime }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  agentCount: {
    type: Number,
    default: 0
  },
  executionTime: {
    type: Number,
    default: 0
  }
})

const formattedTime = computed(() => {
  return `${props.executionTime.toFixed(2)}s`
})
</script>
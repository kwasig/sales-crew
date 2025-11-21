<template>
  <div class="p-4 border-t border-gray-200 bg-gray-50">
    <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
      Usage Stats
    </h3>
    <div class="space-y-2">
      <div class="flex justify-between items-center text-sm">
        <span class="text-gray-600">Agents Active</span>
        <span class="font-medium text-gray-900">{{ agentCount }}</span>
      </div>
      <div class="flex justify-between items-center text-sm">
        <span class="text-gray-600">Tasks Completed</span>
        <span class="font-medium text-gray-900">{{ taskCount }}</span>
      </div>
      <div v-if="totalTokens > 0" class="flex justify-between items-center text-sm">
        <span class="text-gray-600">Total Tokens</span>
        <span class="font-medium text-gray-900">{{ formatNumber(totalTokens) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  agentCount: {
    type: Number,
    default: 0
  },
  taskCount: {
    type: Number,
    default: 0
  },
  totalTokens: {
    type: Number,
    default: 0
  }
})

const formatNumber = (num) => {
  return new Intl.NumberFormat('en-US').format(num)
}
</script>
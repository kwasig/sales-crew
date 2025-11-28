<template>
  <div class="p-4 border-t border-gray-200 bg-gray-50">
    <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
      Usage Metrics
    </h3>
    <div class="space-y-2">
      <div class="flex justify-between items-center text-sm">
        <span class="text-gray-600">Agents Used</span>
        <span class="font-medium text-gray-900">{{ usage?.agents_used || 0 }}</span>
      </div>
      <div class="flex justify-between items-center text-sm">
        <span class="text-gray-600">Total Tasks</span>
        <span class="font-medium text-gray-900">{{ usage?.total_tasks || 0 }}</span>
      </div>
      <div class="flex justify-between items-center text-sm">
        <span class="text-gray-600">Model</span>
        <span class="font-medium text-gray-900">{{ usage?.model || 'N/A' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  usage: {
    type: Object,
    default: () => ({})
  }
})
</script>
<template>
  <div class="p-4 border-t border-gray-200 bg-gray-50" v-if="usage">
    <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
      Usage Metrics
    </h3>
    <div class="space-y-2">
      <div class="flex justify-between items-center text-sm">
        <span class="text-gray-600">Agents Used</span>
        <span class="font-medium text-gray-900">{{ usage.agentCount }}</span>
      </div>
      <div class="flex justify-between items-center text-sm">
        <span class="text-gray-600">Total Tokens</span>
        <span class="font-medium text-gray-900">{{ formatNumber(usage.totalTokens) }}</span>
      </div>
      <div class="flex justify-between items-center text-sm" v-if="usage.promptTokens">
        <span class="text-gray-600">Prompt Tokens</span>
        <span class="font-medium text-gray-900">{{ formatNumber(usage.promptTokens) }}</span>
      </div>
      <div class="flex justify-between items-center text-sm" v-if="usage.completionTokens">
        <span class="text-gray-600">Completion Tokens</span>
        <span class="font-medium text-gray-900">{{ formatNumber(usage.completionTokens) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  usage: {
    type: Object,
    default: null
  }
})

const formatNumber = (num) => {
  if (num === undefined || num === null) return '0'
  return new Intl.NumberFormat().format(num)
}
</script>
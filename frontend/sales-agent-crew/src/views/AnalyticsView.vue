<template>
  <div class="analytics-view">
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-6xl mx-auto">
        <!-- Header -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900">Usage Analytics</h1>
          <p class="text-gray-600 mt-2">Monitor search activity, API usage, and system performance</p>
        </div>

        <!-- Analytics Dashboard -->
        <AnalyticsDashboard />
      </div>
    </div>
  </div>
</template>

<script setup>
import AnalyticsDashboard from '../components/AnalyticsDashboard.vue'
</script>

<style scoped>
.analytics-view {
  min-height: 100vh;
  background-color: #f9fafb;
}
</style>
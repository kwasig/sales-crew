<template>
  <div class="usage-component" v-if="usageMetrics">
    <div class="usage-header">
      <h3 class="usage-title">Agent Usage</h3>
    </div>
    
    <div class="usage-stats">
      <div class="stat-item">
        <span class="stat-label">Total Tokens</span>
        <span class="stat-value">{{ usageMetrics.total_tokens || 0 }}</span>
      </div>
      
      <div class="stat-item">
        <span class="stat-label">Prompt Tokens</span>
        <span class="stat-value">{{ usageMetrics.prompt_tokens || 0 }}</span>
      </div>
      
      <div class="stat-item">
        <span class="stat-label">Completion Tokens</span>
        <span class="stat-value">{{ usageMetrics.completion_tokens || 0 }}</span>
      </div>
      
      <div class="stat-item">
        <span class="stat-label">Agents Used</span>
        <span class="stat-value">{{ usageMetrics.agent_count || 0 }}</span>
      </div>
      
      <div class="stat-item">
        <span class="stat-label">Tasks Executed</span>
        <span class="stat-value">{{ usageMetrics.task_count || 0 }}</span>
      </div>
      
      <div class="stat-item">
        <span class="stat-label">Execution Time</span>
        <span class="stat-value">{{ usageMetrics.execution_time || 0 }}s</span>
      </div>
      
      <div class="stat-item">
        <span class="stat-label">Successful Requests</span>
        <span class="stat-value">{{ usageMetrics.successful_requests || 0 }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UsageComponent',
  props: {
    usageMetrics: {
      type: Object,
      default: () => ({})
    }
  }
}
</script>

<style scoped>
.usage-component {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  margin: 16px 0;
  border: 1px solid #e9ecef;
}

.usage-header {
  margin-bottom: 12px;
}

.usage-title {
  font-size: 14px;
  font-weight: 600;
  color: #495057;
  margin: 0;
}

.usage-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 0;
}

.stat-label {
  font-size: 12px;
  color: #6c757d;
  font-weight: 500;
}

.stat-value {
  font-size: 12px;
  font-weight: 600;
  color: #495057;
  background: #e9ecef;
  padding: 2px 6px;
  border-radius: 4px;
  min-width: 40px;
  text-align: center;
}
</style>
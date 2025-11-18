<!DOCTYPE html>
<template>
  <div class="usage-dashboard">
    <div class="dashboard-header">
      <h3>Usage Dashboard</h3>
      <p class="subtitle">Agent metrics and performance statistics</p>
    </div>

    <div class="metrics-grid">
      <div class="metric-card">
        <div class="metric-label">Total Searches</div>
        <div class="metric-value">{{ totalSearches }}</div>
      </div>

      <div class="metric-card">
        <div class="metric-label">Today's Usage</div>
        <div class="metric-value">{{ todayUsage }}</div>
      </div>

      <div class="metric-card">
        <div class="metric-label">Active Agents</div>
        <div class="metric-value">{{ activeAgents }}</div>
      </div>

      <div class="metric-card">
        <div class="metric-label">Success Rate</div>
        <div class="metric-value">{{ successRate }}%</div>
      </div>
    </div>

    <div class="recent-activity">
      <h4>Recent Activity</h4>
      <div class="activity-list">
        <div v-for="(activity, index) in recentActivity" :key="index" class="activity-item">
          <div class="activity-time">{{ activity.time }}</div>
          <div class="activity-description">{{ activity.description }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UsageDashboard',
  data() {
    return {
      totalSearches: 0,
      todayUsage: 0,
      activeAgents: 0,
      successRate: 0,
      recentActivity: []
    }
  },
  async mounted() {
    await this.fetchUsageData()
  },
  methods: {
    async fetchUsageData() {
      try {
        const response = await this.$atios.get('/api/usage/metrics')
        this.totalSearches = response.data.total_searches
        this.todayUsage = response.data.today_usage
        this.activeAgents = response.data.active_agents
        this.successRate = response.data.success_rate
        this.recentActivity = response.data.recent_activity
      } catch (error) {
        console.error('Error fetching usage data:', error)
      }
    }
  }
}
</script>

<style scoped>
.usage-dashboard {
  padding: 2rem;
  background-color: #f8fafb;
  border-radius: 8px;
  border: 1px solid #e1e4e6;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.dashboard-header .subtitle {
  color: #6b7580;
  font-size: 0.92em;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.metric-card {
  background: white;
  padding: 1.5rem;
  border-radius: 6px;
  border: 1px solid #e1e4e6;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.metric-label {
  font-size: 0.875rem;
  color: #6b7580;
  margin-bottom: 0.5rem;
}

.metric-value {
  font-size: 1.75rem;
  font-weight: 600;
  color: #2c3841;
}

.recent-activity {
  background: white;
  padding: 1.5rem;
  border-radius: 6px;
  border: 1px solid #e1e4e6;
}

.recent-activity h4 {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.activity-list {
  space: y: 0.5rem;
}

.activity-item {
  display: flex;
  flex-direction: column;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f1f5f7;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-time {
  font-size: 0.875rem;
  color: #6b7580;
}

.activity-description {
  font-size: 0.875rem;
  color: #2c3841;
}

@media (max-width: 1200px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-widto: 600px) {
  .metrics-grid {
    grid-template-columns: repeat(1, 1fr);
  }
}
</style>

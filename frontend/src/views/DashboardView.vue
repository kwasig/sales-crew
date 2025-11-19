<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1>Usage Dashboard</h1>
      <p>Real-time analytics and system performance metrics</p>
    </div>

    <!-- Overview Cards -->
    <div class="overview-grid">
      <div class="metric-card">
        <div class="metric-icon">👥</div>
        <div class="metric-content">
          <h3>{{ metrics.overview?.total_sessions || 0 }}</h3>
          <p>Total Sessions</p>
        </div>
      </div>
      
      <div class="metric-card">
        <div class="metric-icon">🔍</div>
        <div class="metric-content">
          <h3>{{ metrics.overview?.total_searches || 0 }}</h3>
          <p>Total Searches</p>
        </div>
      </div>
      
      <div class="metric-card">
        <div class="metric-icon">✅</div>
        <div class="metric-content">
          <h3>{{ metrics.overview?.success_rate || 0 }}%</h3>
          <p>Success Rate</p>
        </div>
      </div>
      
      <div class="metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-content">
          <h3>{{ metrics.overview?.average_searches_per_session || 0 }}</h3>
          <p>Avg Searches/Session</p>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="charts-section">
      <div class="chart-container">
        <h3>Search Activity (Last 7 Days)</h3>
        <div class="chart-placeholder">
          <p>Chart: Daily search activity visualization</p>
          <div class="chart-bars">
            <div v-for="(count, day) in analytics.searches_by_day" :key="day" class="chart-bar">
              <div class="bar" :style="{ height: (count / maxDailySearches) * 100 + '%' }"></div>
              <span class="bar-label">{{ day.split('-')[2] }}</span>
              <span class="bar-count">{{ count }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="chart-container">
        <h3>Top Companies</h3>
        <div class="companies-list">
          <div v-for="company in metrics.top_companies" :key="company.name" class="company-item">
            <span class="company-name">{{ company.name }}</span>
            <span class="search-count">{{ company.searches }} searches</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="activity-section">
      <h3>Recent Searches</h3>
      <div class="activity-list">
        <div v-for="search in metrics.recent_searches" :key="search.timestamp" class="activity-item">
          <div class="activity-icon">{{ search.success ? '✅' : '❌' }}</div>
          <div class="activity-details">
            <strong>{{ search.company_name }}</strong>
            <span>{{ formatDate(search.timestamp) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Financial Insights Section -->
    <div class="financial-section">
      <h3>Financial Analysis Insights</h3>
      <div class="insights-grid">
        <div class="insight-card">
          <h4>Total Analyses</h4>
          <p class="insight-value">{{ financialInsights.total_analyses || 0 }}</p>
        </div>
        <div class="insight-card">
          <h4>Average Sentiment</h4>
          <p class="insight-value">{{ financialInsights.average_sentiment || 'Neutral' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from '../stores/store'

export default {
  name: 'DashboardView',
  setup() {
    const store = useStore()
    const metrics = ref({})
    const analytics = ref({})
    const financialInsights = ref({})
    const loading = ref(true)

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString()
    }

    const fetchDashboardData = async () => {
      try {
        // Fetch metrics
        const metricsResponse = await fetch(`${store.backendUrl}/dashboard/metrics`)
        if (metricsResponse.ok) {
          const data = await metricsResponse.json()
          metrics.value = data.data
        }

        // Fetch analytics
        const analyticsResponse = await fetch(`${store.backendUrl}/dashboard/analytics/7`)
        if (analyticsResponse.ok) {
          const data = await analyticsResponse.json()
          analytics.value = data.data
        }

        // Fetch financial insights
        const insightsResponse = await fetch(`${store.backendUrl}/dashboard/financial-insights`)
        if (insightsResponse.ok) {
          const data = await insightsResponse.json()
          financialInsights.value = data.data
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchDashboardData()
    })

    return {
      metrics,
      analytics,
      financialInsights,
      loading,
      formatDate,
      maxDailySearches: Math.max(...Object.values(analytics.value.searches_by_day || {}))
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 3rem;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.dashboard-header p {
  color: #6b7280;
  font-size: 1.2rem;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.metric-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.metric-icon {
  font-size: 2.5rem;
}

.metric-content h3 {
  font-size: 2rem;
  color: #1f2937;
  margin: 0;
}

.metric-content p {
  color: #6b7280;
  margin: 0;
}

.charts-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  margin-bottom: 3rem;
}

.chart-container {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.chart-placeholder {
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #6b7280;
}

.chart-bars {
  display: flex;
  gap: 1rem;
  align-items: end;
  height: 100px;
  margin-top: 1rem;
}

.chart-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.bar {
  width: 30px;
  background: #3b82f6;
  border-radius: 4px;
  min-height: 20px;
}

.bar-label {
  font-size: 0.8rem;
  color: #6b7280;
}

.bar-count {
  font-size: 0.7rem;
  color: #9ca3af;
}

.companies-list {
  max-height: 200px;
  overflow-y: auto;
}

.company-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.company-name {
  font-weight: 500;
}

.search-count {
  color: #6b7280;
  font-size: 0.9rem;
}

.activity-section,
.financial-section {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.activity-list {
  max-height: 300px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.activity-icon {
  font-size: 1.2rem;
}

.activity-details {
  display: flex;
  flex-direction: column;
}

.activity-details span {
  font-size: 0.9rem;
  color: #6b7280;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.insight-card {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
}

.insight-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #3b82f6;
  margin: 0.5rem 0 0 0;
}
</style>
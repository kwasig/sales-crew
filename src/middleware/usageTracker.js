const development = process.env.NODE_ENV !== 'production'

const usageTracker = () => {
  const usageData = {
    totalSearches: 0,
    todayUsage: 0,
    activeAgents: 0,
    successRate: 0,
    recentActivity: []
  }

  // Simulated usage data for development
  if (development) {
    usageData = {
      totalSearches: 1247,
      todayUsage: 23,
      activeAgents: 5,
      successRate: 86,
      recentActivity: [
        { time: '2:30 PM', description: 'Agent #1 performed search' },
        { time: '2:15 PM', description: 'Agent #2 completed task' },
        { time: '1:45 PM', description: 'Agent #3 started session' },
        { time: '1:30 PM', description: 'Agent #4 updated profile' },
        { time: '12:45 PM', description: 'Agent #5 completed analysis' }
      ]
    }
  }

  return {
    getMetrics: () => {
      return {
        total_searches: usageData.totalSearches,
        today_usage: usageData.todayUsage,
        active_agents: usageData.activeAgents,
        success_rate: usageData.successRate,
        recent_activity: usageData.recentActivity
      }
    },

    trackSearch: (agentId) => {
      if (development) {
        usageData.totalSearches += 1
        usageData.todayUsage += 1
        console.log(`Tracked search for agent ${agentId}`)
      }
    },

    trackActivity: (activity) => {
      if (development) {
        usageData.recentActivity.unshift(activity)
        // Keep only the last 5 activities
        if (usageData.recentActivity.length > 5) {
          usageData.recentActivity = usageData.recentActivity.slice(0, 5)
        }
      }
    }
  }
}

module.exports = usageTracker
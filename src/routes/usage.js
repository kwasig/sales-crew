// Add usage api route
app.get('/api/usage/metrics', (req, res) => {
  try {
    const usageTracker = require('../middleware/usageTracker')
    const metrics = usageTracker().getMetrics()
    res.json(metrics)
  } catch (error) {
    console.error('Error fetching usage metrics:', error)
    res.status(500).json({ error: 'Failed to fetch usage metrics' })
  }
})
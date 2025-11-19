// src/services/analytics.js
import axios from 'axios'

// Use environment variable for the analytics API base URL
const ANALYTICS_API_URL = import.meta.env.PROD 
  ? `${window.location.origin}/analytics`  // Use the current origin in production
  : (import.meta.env.VITE_ANALYTICS_API_URL || 'http://localhost:8002')

const analyticsApi = axios.create({
  baseURL: ANALYTICS_API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const getAnalytics = async (startDate, endDate) => {
  try {
    // If both dates are provided, use the range endpoint
    if (startDate && endDate) {
      const response = await analyticsApi.post('/analytics/range', {
        start_date: startDate,
        end_date: endDate
      })
      return response.data
    } else {
      // Otherwise, get daily analytics
      const response = await analyticsApi.get(`/analytics/daily?target_date=${startDate || ''}`)
      return response.data
    }
  } catch (error) {
    console.error('Analytics API error:', error)
    throw error
  }
}

export const trackSearchSession = async (sessionData) => {
  try {
    // This would typically send tracking data to the backend
    // For now, we'll log it and handle it locally
    console.log('Tracking search session:', sessionData)
    
    // In a real implementation, you would send this to your backend
    // await analyticsApi.post('/track', sessionData)
    
    return { success: true }
  } catch (error) {
    console.error('Error tracking search session:', error)
    // Don't throw the error to avoid breaking the main search functionality
    return { success: false, error: error.message }
  }
}

export default analyticsApi
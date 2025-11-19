// src/services/api.js
import axios from 'axios'

// Use environment variable for the API base URL
const API_URL = import.meta.env.PROD 
  ? `${window.location.origin}/api`  // Use the current origin in production
  : (import.meta.env.VITE_API_URL || 'http://localhost:8000')

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const generateLeads = async (prompt, keys) => {
  try {
    if (!keys?.sambanovaKey || !keys?.exaKey) {
      throw new Error('API keys are required')
    }

    const response = await api.post('/generate-leads', 
      { prompt },
      {
        headers: {
          'x-sambanova-key': keys.sambanovaKey,
          'x-exa-key': keys.exaKey
        }
      }
    )
    return response.data
  } catch (error) {
    console.error('API error:', error)
    throw error
  }
}

export const getFinancialAnalysis = async (params, exaKey) => {
  try {
    if (!exaKey) {
      throw new Error('Exa API key is required')
    }

    const response = await api.post('/financial/financial-analysis', 
      params,
      {
        headers: {
          'x-exa-key': exaKey
        }
      }
    )
    return response.data
  } catch (error) {
    console.error('Financial analysis API error:', error)
    throw error
  }
}

export const getUsageSummary = async () => {
  try {
    const response = await api.get('/api/usage/summary')
    return response.data
  } catch (error) {
    console.error('Usage dashboard API error:', error)
    throw error
  }
}

export const getSystemHealth = async () => {
  try {
    const response = await api.get('/api/usage/health')
    return response.data
  } catch (error) {
    console.error('System health API error:', error)
    throw error
  }
}

export const getPopularSearches = async (limit = 10) => {
  try {
    const response = await api.get(`/api/usage/searches/popular?limit=${limit}`)
    return response.data
  } catch (error) {
    console.error('Popular searches API error:', error)
    throw error
  }
}

export const getDailyAnalytics = async () => {
  try {
    const response = await api.get('/api/usage/analytics/daily')
    return response.data
  } catch (error) {
    console.error('Daily analytics API error:', error)
    throw error
  }
}

export default api


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
    
    // Handle both old and new response formats
    const responseData = response.data
    
    // If response has usage_metrics, return structured data
    if (responseData.usage_metrics) {
      return {
        outreach_list: responseData.outreach_list || [],
        usage_metrics: responseData.usage_metrics
      }
    }
    
    // Fallback for old format
    return {
      outreach_list: responseData.outreach_list || responseData,
      usage_metrics: {
        agent_count: 5,
        task_count: 6,
        execution_time: 0,
        successful_requests: 1
      }
    }
  } catch (error) {
    console.error('API error:', error)
    throw error
  }
}

export default api


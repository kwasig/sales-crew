// src/services/api.js
import axios from 'axios'
import mixpanel from 'mixpanel-browser'

mixpanel.init(import.meta.env.VITE_MIXPANEL_TOKEN || '')

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

export const trackSignup = (userData) => {
  mixpanel.track('Sign Up', {
    'User ID': userData.id,
    'Email': userData.email,
    'Signup Date': new Date().toISOString()
  })
}

export const trackSignin = (userData) => {
  mixpanel.track('Sign In', {
    'User ID': userData.id,
    'Email': userData.email,
    'Signin Date': new Date().toISOString()
  })
}

export const trackEvent = (eventName, properties = {}) => {
  mixpanel.track(eventName, properties)
}

export const trackPageView = (pageName) => {
  mixpanel.track('Page View', {
    'Page Name': pageName,
    'Timestamp': new Date().toISOString()
  })
}

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

export default api
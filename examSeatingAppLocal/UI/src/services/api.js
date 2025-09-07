import axios from 'axios'
import { useAppStore } from '@/stores/app'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: window.location.protocol + '//' + window.location.hostname + ':8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const appStore = useAppStore()
    appStore.setLoading(true)
    return config
  },
  (error) => {
    const appStore = useAppStore()
    appStore.setLoading(false)
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    const appStore = useAppStore()
    appStore.setLoading(false)
    return response
  },
  (error) => {
    const appStore = useAppStore()
    appStore.setLoading(false)
    
    // Handle common errors with detailed messages
    let message = 'An error occurred'
    
    if (error.response?.data?.detail) {
      // FastAPI error format
      message = error.response.data.detail
    } else if (error.response?.data?.message) {
      // Generic error format
      message = error.response.data.message
    } else if (error.message) {
      // Axios error message
      message = error.message
    }
    
    // Add status code context
    if (error.response?.status) {
      message = `${message} (Status: ${error.response.status})`
    }
    
    appStore.showError(message)
    
    return Promise.reject(error)
  }
)

export default api

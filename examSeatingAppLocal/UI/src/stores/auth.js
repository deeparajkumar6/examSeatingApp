import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const loading = ref(false)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const currentUser = computed(() => user.value)

  // Actions
  const login = async (credentials) => {
    try {
      loading.value = true
      const response = await api.post('/auth/login', credentials)
      
      token.value = response.data.token
      user.value = response.data.user
      
      localStorage.setItem('token', token.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      
      return response.data
    } catch (error) {
      throw error
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const initializeAuth = () => {
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken && storedUser) {
      token.value = storedToken
      user.value = JSON.parse(storedUser)
    }
  }

  return {
    // State
    user,
    token,
    loading,
    
    // Getters
    isAuthenticated,
    currentUser,
    
    // Actions
    login,
    logout,
    initializeAuth
  }
})
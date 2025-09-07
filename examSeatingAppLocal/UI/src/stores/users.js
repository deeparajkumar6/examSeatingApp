import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'
import { useAppStore } from './app'

export const useUsersStore = defineStore('users', () => {
  // State
  const users = ref([])
  const loading = ref(false)

  // Actions
  const fetchUsers = async () => {
    try {
      loading.value = true
      const response = await api.get('/auth/users')
      users.value = response.data.users || []
    } catch (error) {
      console.error('Failed to fetch users:', error)
      users.value = []
    } finally {
      loading.value = false
    }
  }

  const createUser = async (userData) => {
    try {
      const appStore = useAppStore()
      await api.post('/auth/users', userData)
      await fetchUsers() // Refresh the list
      appStore.showSuccess('User created successfully')
    } catch (error) {
      console.error('Failed to create user:', error)
      throw error
    }
  }

  const deleteUser = async (userId) => {
    try {
      const appStore = useAppStore()
      await api.delete(`/auth/users/${userId}`)
      await fetchUsers() // Refresh the list
      appStore.showSuccess('User deleted successfully')
    } catch (error) {
      console.error('Failed to delete user:', error)
      throw error
    }
  }

  return {
    // State
    users,
    loading,
    
    // Actions
    fetchUsers,
    createUser,
    deleteUser
  }
})
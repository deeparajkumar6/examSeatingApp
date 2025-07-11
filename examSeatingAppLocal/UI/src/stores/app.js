import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  // State
  const title = ref('Exam Seating Scheduler')
  const loading = ref(false)
  const snackbar = ref({
    show: false,
    message: '',
    color: 'success',
    timeout: 3000
  })

  // Getters
  const isLoading = computed(() => loading.value)

  // Actions
  const setLoading = (state) => {
    loading.value = state
  }

  const showSnackbar = (message, color = 'success', timeout = 3000) => {
    snackbar.value = {
      show: true,
      message,
      color,
      timeout
    }
  }

  const hideSnackbar = () => {
    snackbar.value.show = false
  }

  const showSuccess = (message) => showSnackbar(message, 'success')
  const showError = (message) => showSnackbar(message, 'error')
  const showWarning = (message) => showSnackbar(message, 'warning')
  const showInfo = (message) => showSnackbar(message, 'info')

  return {
    // State
    title,
    loading,
    snackbar,

    // Getters
    isLoading,

    // Actions
    setLoading,
    showSnackbar,
    hideSnackbar,
    showSuccess,
    showError,
    showWarning,
    showInfo
  }
})

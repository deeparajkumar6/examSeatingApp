import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { classesApi } from '@/services/classesApi'
import { useAppStore } from './app'

export const useClassesStore = defineStore('classes', () => {
  // State
  const classes = ref([])
  const loading = ref(false)

  // Getters
  const classCount = computed(() => classes.value.length)
  const totalStudents = computed(() => 
    classes.value.reduce((total, cls) => total + cls.students.length, 0)
  )

  // Actions
  const fetchClasses = async () => {
    try {
      loading.value = true
      const response = await classesApi.getAll()
      // Handle both array and object responses
      classes.value = Array.isArray(response) ? response : (response.classes || [])
    } catch (error) {
      console.error('Failed to fetch classes:', error)
      classes.value = []
    } finally {
      loading.value = false
    }
  }

  const createClass = async (classData) => {
    try {
      const appStore = useAppStore()
      await classesApi.create(classData)
      await fetchClasses() // Refresh the list
      appStore.showSuccess('Class created successfully')
    } catch (error) {
      console.error('Failed to create class:', error)
      throw error
    }
  }

  const updateClass = async (classId, classData) => {
    try {
      const appStore = useAppStore()
      await classesApi.update(classId, classData)
      await fetchClasses() // Refresh the list
      appStore.showSuccess('Class updated successfully')
    } catch (error) {
      console.error('Failed to update class:', error)
      throw error
    }
  }

  const deleteClass = async (classId) => {
    try {
      const appStore = useAppStore()
      await classesApi.delete(classId)
      await fetchClasses() // Refresh the list
      appStore.showSuccess('Class deleted successfully')
    } catch (error) {
      console.error('Failed to delete class:', error)
      throw error
    }
  }

  return {
    // State
    classes,
    loading,
    
    // Getters
    classCount,
    totalStudents,
    
    // Actions
    fetchClasses,
    createClass,
    updateClass,
    deleteClass
  }
})

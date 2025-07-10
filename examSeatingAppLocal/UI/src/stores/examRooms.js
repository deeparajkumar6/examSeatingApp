import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { examRoomsApi } from '@/services/examRoomsApi'
import { useAppStore } from './app'

export const useExamRoomsStore = defineStore('examRooms', () => {
  // State
  const examRooms = ref([])
  const loading = ref(false)

  // Getters
  const roomCount = computed(() => examRooms.value.length)
  const totalCapacity = computed(() => 
    examRooms.value.reduce((total, room) => total + room.roomCapacity, 0)
  )

  // Actions
  const fetchExamRooms = async () => {
    try {
      loading.value = true
      const response = await examRoomsApi.getAll()
      // Handle both array and object responses
      examRooms.value = Array.isArray(response) ? response : (response.examRooms || [])
    } catch (error) {
      console.error('Failed to fetch exam rooms:', error)
      examRooms.value = []
    } finally {
      loading.value = false
    }
  }

  const createExamRoom = async (roomData) => {
    try {
      const appStore = useAppStore()
      await examRoomsApi.create(roomData)
      await fetchExamRooms() // Refresh the list
      appStore.showSuccess('Exam room created successfully')
    } catch (error) {
      console.error('Failed to create exam room:', error)
      throw error
    }
  }

  const updateExamRoom = async (roomId, roomData) => {
    try {
      const appStore = useAppStore()
      await examRoomsApi.update(roomId, roomData)
      await fetchExamRooms() // Refresh the list
      appStore.showSuccess('Exam room updated successfully')
    } catch (error) {
      console.error('Failed to update exam room:', error)
      throw error
    }
  }

  const deleteExamRoom = async (roomId) => {
    try {
      const appStore = useAppStore()
      await examRoomsApi.delete(roomId)
      await fetchExamRooms() // Refresh the list
      appStore.showSuccess('Exam room deleted successfully')
    } catch (error) {
      console.error('Failed to delete exam room:', error)
      throw error
    }
  }

  return {
    // State
    examRooms,
    loading,
    
    // Getters
    roomCount,
    totalCapacity,
    
    // Actions
    fetchExamRooms,
    createExamRoom,
    updateExamRoom,
    deleteExamRoom
  }
})

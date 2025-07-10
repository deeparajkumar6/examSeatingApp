import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { scheduleApi } from '@/services/scheduleApi'
import { useAppStore } from './app'
import PDFService from '@/services/pdfService'

export const useScheduleStore = defineStore('schedule', () => {
  // State
  const currentSchedule = ref(null)
  const loading = ref(false)
  const scheduleHistory = ref([])

  // Getters
  const hasSchedule = computed(() => !!currentSchedule.value)
  const totalStudentsScheduled = computed(() => {
    if (!currentSchedule.value?.room_assignments) return 0
    return currentSchedule.value.room_assignments.reduce(
      (total, room) => total + (room.students?.length || 0), 0
    )
  })

  // Actions
  const createSchedule = async (scheduleData) => {
    try {
      loading.value = true
      const appStore = useAppStore()
      
      const result = await scheduleApi.create(scheduleData)
      currentSchedule.value = result
      
      // Add to history
      scheduleHistory.value.unshift({
        ...result,
        createdAt: new Date().toISOString()
      })
      
      appStore.showSuccess(`Schedule created successfully! ${totalStudentsScheduled.value} students assigned.`)
    } catch (error) {
      console.error('Failed to create schedule:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const clearSchedule = () => {
    currentSchedule.value = null
  }

  const exportSummaryPDF = async () => {
    if (!currentSchedule.value) return
    
    try {
      await PDFService.generateSummaryPDF(currentSchedule.value)
      const appStore = useAppStore()
      appStore.showSuccess('Summary PDF generated successfully')
    } catch (error) {
      console.error('Failed to generate summary PDF:', error)
      const appStore = useAppStore()
      appStore.showError('Failed to generate summary PDF')
    }
  }

  const exportDetailedPDF = async () => {
    if (!currentSchedule.value) return
    
    try {
      await PDFService.generateDetailedPDF(currentSchedule.value)
      const appStore = useAppStore()
      appStore.showSuccess('Detailed PDF generated successfully')
    } catch (error) {
      console.error('Failed to generate detailed PDF:', error)
      const appStore = useAppStore()
      appStore.showError('Failed to generate detailed PDF')
    }
  }

  // Legacy method for backward compatibility
  const exportToPdf = async () => {
    await exportSummaryPDF()
  }

  return {
    // State
    currentSchedule,
    loading,
    scheduleHistory,
    
    // Getters
    hasSchedule,
    totalStudentsScheduled,
    
    // Actions
    createSchedule,
    clearSchedule,
    exportSummaryPDF,
    exportDetailedPDF,
    exportToPdf // Legacy method
  }
})

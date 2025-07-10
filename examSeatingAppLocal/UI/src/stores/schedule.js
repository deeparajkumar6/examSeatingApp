import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { scheduleApi } from '@/services/scheduleApi'
import { useAppStore } from './app'

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

  const exportToPdf = () => {
    if (!currentSchedule.value) return
    
    try {
      // Create PDF export functionality
      const printWindow = window.open('', '_blank')
      const scheduleHtml = generateScheduleHtml(currentSchedule.value)
      
      printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
          <title>Exam Schedule - ${currentSchedule.value.title}</title>
          <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .header { text-align: center; margin-bottom: 30px; }
            .room-section { margin-bottom: 30px; page-break-inside: avoid; }
            .room-header { background: #f5f5f5; padding: 10px; font-weight: bold; }
            .student-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            .student-table th, .student-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            .student-table th { background: #f9f9f9; }
            @media print { .no-print { display: none; } }
          </style>
        </head>
        <body>
          ${scheduleHtml}
          <div class="no-print" style="margin-top: 20px;">
            <button onclick="window.print()">Print</button>
            <button onclick="window.close()">Close</button>
          </div>
        </body>
        </html>
      `)
      
      printWindow.document.close()
      
      const appStore = useAppStore()
      appStore.showSuccess('Schedule opened in new window for printing/PDF export')
    } catch (error) {
      console.error('Failed to export PDF:', error)
      const appStore = useAppStore()
      appStore.showError('Failed to export schedule')
    }
  }

  const generateScheduleHtml = (schedule) => {
    if (!schedule?.room_assignments) return '<p>No schedule data available</p>'
    
    let html = `
      <div class="header">
        <h1>${schedule.title || 'Exam Schedule'}</h1>
        <p><strong>Date:</strong> ${schedule.date || 'N/A'} | <strong>Session:</strong> ${schedule.session || 'N/A'}</p>
        <p><strong>Total Students:</strong> ${totalStudentsScheduled.value}</p>
      </div>
    `
    
    schedule.room_assignments.forEach(room => {
      if (!room) return
      
      html += `
        <div class="room-section">
          <div class="room-header">
            ${room.room_number || 'Unknown Room'} - ${room.room_building || 'Unknown Building'} (${room.room_floor || 'Unknown Floor'})
            <span style="float: right;">Capacity: ${room.room_capacity || 0} | Assigned: ${room.students?.length || 0}</span>
          </div>
          <table class="student-table">
            <thead>
              <tr>
                <th>Roll Number</th>
                <th>Student Name</th>
                <th>Class</th>
              </tr>
            </thead>
            <tbody>
      `
      
      if (room.students && room.students.length > 0) {
        room.students.forEach(student => {
          if (student) {
            html += `
              <tr>
                <td>${student.rollNumber || 'N/A'}</td>
                <td>${student.studentName || 'N/A'}</td>
                <td>${student.className || 'N/A'}</td>
              </tr>
            `
          }
        })
      } else {
        html += `
          <tr>
            <td colspan="3" style="text-align: center; font-style: italic;">No students assigned</td>
          </tr>
        `
      }
      
      html += `
            </tbody>
          </table>
        </div>
      `
    })
    
    return html
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
    exportToPdf
  }
})

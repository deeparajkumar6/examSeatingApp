import api from './api'

export class ExcelExportService {
  /**
   * Export summary Excel
   */
  static async exportSummaryExcel(scheduleData) {
    try {
      const response = await api.post('/schedule/export/excel/summary', scheduleData, {
        responseType: 'blob'
      })
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      
      // Get filename from response headers or create default
      const contentDisposition = response.headers['content-disposition']
      let filename = 'Exam_Summary.xlsx'
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/)
        if (filenameMatch) {
          filename = filenameMatch[1]
        }
      }
      
      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      
      return { success: true }
    } catch (error) {
      console.error('Excel export failed:', error)
      throw new Error('Failed to export Excel file')
    }
  }

  /**
   * Export detailed Excel
   */
  static async exportDetailedExcel(scheduleData) {
    try {
      const response = await api.post('/schedule/export/excel/detailed', scheduleData, {
        responseType: 'blob'
      })
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      
      // Get filename from response headers or create default
      const contentDisposition = response.headers['content-disposition']
      let filename = 'Exam_Detailed.xlsx'
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/)
        if (filenameMatch) {
          filename = filenameMatch[1]
        }
      }
      
      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      
      return { success: true }
    } catch (error) {
      console.error('Excel export failed:', error)
      throw new Error('Failed to export Excel file')
    }
  }
}

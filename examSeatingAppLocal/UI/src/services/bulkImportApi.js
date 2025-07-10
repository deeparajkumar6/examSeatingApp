import api from './api'

export const bulkImportApi = {
  // Validate Excel file without importing
  async validateExcel(file) {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post('/bulk-import/validate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  // Import Excel file
  async importExcel(file) {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post('/bulk-import/excel', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  // Get template information
  async getTemplate() {
    const response = await api.get('/bulk-import/template')
    return response.data
  }
}

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

  // Import selected classes from Excel file
  async selectiveImportExcel(file, selectedClassData) {
    const formData = new FormData()
    formData.append("file", file)
    formData.append("selected_classes", JSON.stringify(selectedClassData))
    
    const response = await api.post("/bulk-import/excel/selective", formData, {
      headers: {
        "Content-Type": "multipart/form-data"
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

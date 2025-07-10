import api from './api'

export const classesApi = {
  // Get all classes
  async getAll() {
    const response = await api.get('/class')
    return response.data
  },

  // Create new class
  async create(classData) {
    const response = await api.post('/class', classData)
    return response.data
  },

  // Update class
  async update(id, classData) {
    const response = await api.put(`/class/${id}`, classData)
    return response.data
  },

  // Delete class
  async delete(id) {
    const response = await api.delete(`/class/${id}`)
    return response.data
  }
}

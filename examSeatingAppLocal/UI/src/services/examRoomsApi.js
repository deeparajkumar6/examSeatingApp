import api from './api'

export const examRoomsApi = {
  // Get all exam rooms
  async getAll() {
    const response = await api.get('/examRoom')
    return response.data
  },

  // Create new exam room
  async create(roomData) {
    const response = await api.post('/examRoom', roomData)
    return response.data
  },

  // Update exam room
  async update(id, roomData) {
    const response = await api.put(`/examRoom/${id}`, roomData)
    return response.data
  },

  // Delete exam room
  async delete(id) {
    const response = await api.delete(`/examRoom/${id}`)
    return response.data
  }
}

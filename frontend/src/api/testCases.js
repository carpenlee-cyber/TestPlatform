import api from './index'

export const testCaseApi = {
  getAll() {
    return api.get('/test-cases')
  },
  
  getById(id) {
    return api.get(`/test-cases/${id}`)
  },
  
  create(data) {
    return api.post('/test-cases', data)
  },
  
  update(id, data) {
    return api.put(`/test-cases/${id}`, data)
  },
  
  delete(id) {
    return api.delete(`/test-cases/${id}`)
  },
  
  getByStatus(status) {
    return api.get(`/test-cases/status/${status}`)
  }
}

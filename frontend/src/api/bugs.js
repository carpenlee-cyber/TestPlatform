import api from './index'

export const bugApi = {
  getAll() {
    return api.get('/bugs')
  },
  
  getById(id) {
    return api.get(`/bugs/${id}`)
  },
  
  create(data) {
    return api.post('/bugs', data)
  },
  
  update(id, data) {
    return api.put(`/bugs/${id}`, data)
  },
  
  delete(id) {
    return api.delete(`/bugs/${id}`)
  },
  
  getByStatus(status) {
    return api.get(`/bugs/status/${status}`)
  }
}

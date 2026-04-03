import api from './index'

export const authApi = {
  login(credentials) {
    return api.post('/auth/login', credentials)
  },
  
  register(data) {
    return api.post('/auth/register', data)
  }
}

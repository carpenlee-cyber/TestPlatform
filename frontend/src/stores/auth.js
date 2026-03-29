import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('tp_token') || '')
  const user = ref(JSON.parse(localStorage.getItem('tp_user') || '{}'))
  
  const isLoggedIn = computed(() => !!token.value)
  const username = computed(() => user.value.username || '')
  const role = computed(() => user.value.role || '')
  
  function setAuth(authToken, userData) {
    token.value = authToken
    user.value = userData
    localStorage.setItem('tp_token', authToken)
    localStorage.setItem('tp_user', JSON.stringify(userData))
  }
  
  function logout() {
    token.value = ''
    user.value = {}
    localStorage.removeItem('tp_token')
    localStorage.removeItem('tp_user')
  }
  
  return {
    token,
    user,
    isLoggedIn,
    username,
    role,
    setAuth,
    logout
  }
})

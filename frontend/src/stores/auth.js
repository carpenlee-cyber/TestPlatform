import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref(localStorage.getItem('tp_token') || sessionStorage.getItem('tp_token') || '')
  const user = ref(JSON.parse(localStorage.getItem('tp_user') || sessionStorage.getItem('tp_user') || '{}'))
  
  // Getters
  const isLoggedIn = computed(() => !!token.value)
  const username = computed(() => user.value.username || '')
  const role = computed(() => user.value.role || '')
  
  // Actions
  /**
   * 设置认证信息
   * @param {string} authToken - JWT token
   * @param {Object} userData - 用户信息
   * @param {boolean} rememberMe - 是否记住登录状态（使用 localStorage 否则使用 sessionStorage）
   */
  function setAuth(authToken, userData, rememberMe = false) {
    token.value = authToken
    user.value = userData
    
    const storage = rememberMe ? localStorage : sessionStorage
    const otherStorage = rememberMe ? sessionStorage : localStorage
    
    // 存储到选择的 storage
    storage.setItem('tp_token', authToken)
    storage.setItem('tp_user', JSON.stringify(userData))
    
    // 清除另一个 storage 中的数据
    otherStorage.removeItem('tp_token')
    otherStorage.removeItem('tp_user')
  }
  
  /**
   * 退出登录
   */
  function logout() {
    token.value = ''
    user.value = {}
    
    // 清除所有存储
    localStorage.removeItem('tp_token')
    localStorage.removeItem('tp_user')
    sessionStorage.removeItem('tp_token')
    sessionStorage.removeItem('tp_user')
  }
  
  /**
   * 初始化认证状态（用于应用启动时）
   */
  function initAuth() {
    // 优先从 localStorage 读取
    let storedToken = localStorage.getItem('tp_token')
    let storedUser = localStorage.getItem('tp_user')
    
    // 如果没有，尝试从 sessionStorage 读取
    if (!storedToken) {
      storedToken = sessionStorage.getItem('tp_token')
      storedUser = sessionStorage.getItem('tp_user')
    }
    
    if (storedToken) {
      token.value = storedToken
      user.value = JSON.parse(storedUser || '{}')
    }
  }
  
  return {
    token,
    user,
    isLoggedIn,
    username,
    role,
    setAuth,
    logout,
    initAuth
  }
})

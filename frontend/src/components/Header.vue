<template>
  <div class="header">
    <div class="header-left">
      <span class="logo-text">TestPlatform</span>
    </div>
    <div class="header-right">
      <span class="username">{{ username }}</span>
      <el-button type="danger" size="small" @click="handleLogout">
        退出登录
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('Admin')

onMounted(() => {
  const storedUsername = localStorage.getItem('username')
  if (storedUsername) {
    username.value = storedUsername
  }
})

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  router.push('/login')
}
</script>

<style scoped>
.header {
  height: 60px;
  background: linear-gradient(90deg, #409eff 0%, #606266 100%);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
}

.logo-text {
  font-size: 22px;
  font-weight: 600;
  color: #ffffff;
  letter-spacing: 1px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.username {
  font-size: 14px;
  color: #ffffff;
  font-weight: 500;
}
</style>

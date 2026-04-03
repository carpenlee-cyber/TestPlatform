<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside 
      :width="isCollapse ? '64px' : '220px'" 
      class="sidebar"
      :class="{ 'sidebar-collapse': isCollapse }"
    >
      <div class="logo-container">
        <el-icon :size="28" class="logo-icon"><Platform /></el-icon>
        <span v-show="!isCollapse" class="logo-text">TestPlatform</span>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :collapse-transition="false"
        router
        class="sidebar-menu"
        background-color="#001529"
        text-color="#bfcbd9"
        active-text-color="#409eff"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Odometer /></el-icon>
          <template #title>仪表盘</template>
        </el-menu-item>
        
        <el-menu-item index="/test-cases">
          <el-icon><Document /></el-icon>
          <template #title>测试用例</template>
        </el-menu-item>
        
        <el-menu-item index="/bugs">
          <el-icon><CircleClose /></el-icon>
          <template #title>Bug管理</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container class="main-container">
      <!-- 顶部导航栏 -->
      <el-header class="header">
        <div class="header-left">
          <el-button
            type="text"
            class="collapse-btn"
            @click="toggleSidebar"
          >
            <el-icon :size="20">
              <Fold v-if="!isCollapse" />
              <Expand v-else />
            </el-icon>
          </el-button>
          
          <breadcrumb class="breadcrumb" />
        </div>
        
        <div class="header-right">
          <!-- 全屏按钮 -->
          <el-tooltip content="全屏" placement="bottom">
            <el-button type="text" class="header-btn" @click="toggleFullscreen">
              <el-icon :size="18"><FullScreen /></el-icon>
            </el-button>
          </el-tooltip>
          
          <!-- 通知 -->
          <el-tooltip content="通知" placement="bottom">
            <el-button type="text" class="header-btn">
              <el-badge :value="3" class="notification-badge">
                <el-icon :size="18"><Bell /></el-icon>
              </el-badge>
            </el-button>
          </el-tooltip>
          
          <!-- 用户下拉菜单 -->
          <el-dropdown trigger="click" @command="handleCommand">
            <div class="user-info">
              <el-avatar 
                :size="36" 
                :src="userAvatar"
                class="user-avatar"
              >
                {{ userInitials }}
              </el-avatar>
              <span v-show="!isMobile" class="username">{{ authStore.username }}</span>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>个人中心
                </el-dropdown-item>
                <el-dropdown-item command="settings">
                  <el-icon><Setting /></el-icon>系统设置
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 主内容区 -->
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Platform,
  Odometer,
  Document,
  CircleClose,
  Fold,
  Expand,
  FullScreen,
  Bell,
  ArrowDown,
  User,
  Setting,
  SwitchButton
} from '@element-plus/icons-vue'
import { useAuthStore } from '../stores/auth'
import Breadcrumb from '../components/Breadcrumb.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// 侧边栏折叠状态
const isCollapse = ref(false)
const isMobile = ref(false)

// 当前激活的菜单
const activeMenu = computed(() => route.path)

// 用户头像显示文字
const userInitials = computed(() => {
  const name = authStore.username || 'U'
  return name.charAt(0).toUpperCase()
})

// 用户头像（可替换为实际头像URL）
const userAvatar = computed(() => {
  // 如果有头像URL，返回URL，否则返回空字符串让el-avatar显示文字
  return ''
})

// 切换侧边栏
const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}

// 全屏切换
const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}

// 处理用户下拉菜单命令
const handleCommand = async (command) => {
  switch (command) {
    case 'profile':
      ElMessage.info('个人中心功能开发中')
      break
    case 'settings':
      ElMessage.info('系统设置功能开发中')
      break
    case 'logout':
      try {
        await ElMessageBox.confirm(
          '确定要退出登录吗？',
          '提示',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        authStore.logout()
        ElMessage.success('已退出登录')
        router.push('/login')
      } catch {
        // 用户取消
      }
      break
  }
}

// 响应式处理
const handleResize = () => {
  const width = window.innerWidth
  isMobile.value = width < 768
  if (width < 992) {
    isCollapse.value = true
  } else {
    isCollapse.value = false
  }
}

onMounted(() => {
  handleResize()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.layout-container {
  height: 100vh;
  width: 100%;
}

/* 侧边栏样式 */
.sidebar {
  background-color: #001529;
  transition: width 0.3s;
  display: flex;
  flex-direction: column;
}

.logo-container {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.logo-icon {
  color: #409eff;
  flex-shrink: 0;
}

.logo-text {
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  margin-left: 12px;
  white-space: nowrap;
  transition: opacity 0.3s;
}

.sidebar-menu {
  flex: 1;
  border-right: none;
}

.sidebar-menu :deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
}

.sidebar-menu :deep(.el-menu-item:hover) {
  background-color: #1890ff !important;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background-color: #1890ff !important;
}

/* 主容器 */
.main-container {
  background-color: #f0f2f5;
  overflow: hidden;
}

/* 顶部导航栏 */
.header {
  height: 64px;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.collapse-btn {
  color: #606266;
  padding: 8px;
  height: auto;
}

.collapse-btn:hover {
  color: #409eff;
  background-color: #f5f7fa;
}

.breadcrumb {
  font-size: 14px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-btn {
  color: #606266;
  padding: 8px;
  height: auto;
}

.header-btn:hover {
  color: #409eff;
  background-color: #f5f7fa;
}

.notification-badge :deep(.el-badge__content) {
  top: 8px;
  right: 8px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f7fa;
}

.user-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-weight: 600;
}

.username {
  font-size: 14px;
  color: #606266;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-icon {
  color: #909399;
  font-size: 12px;
}

/* 主内容区 */
.main-content {
  padding: 20px;
  overflow-y: auto;
}

/* 页面切换动画 */
.fade-transform-leave-active,
.fade-transform-enter-active {
  transition: all 0.3s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

/* 响应式 */
@media (max-width: 768px) {
  .header {
    padding: 0 16px;
  }
  
  .main-content {
    padding: 16px;
  }
}
</style>

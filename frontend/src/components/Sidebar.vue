<template>
  <div class="sidebar">
    <div class="logo">
      <span class="logo-text">TestPlatform</span>
    </div>
    <el-menu
      :default-active="activeRoute"
      class="sidebar-menu"
      :router="true"
      background-color="#2c3e50"
      text-color="#bfcbd9"
      active-text-color="#409eff"
    >
      <el-menu-item index="/dashboard">
        <el-icon><Odometer /></el-icon>
        <span>仪表盘</span>
      </el-menu-item>
      <el-menu-item index="/test-cases">
        <el-icon><Document /></el-icon>
        <span>测试用例</span>
      </el-menu-item>
      <el-menu-item index="/bugs">
        <el-icon><Warning /></el-icon>
        <span>缺陷管理</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Odometer, Document, Warning } from '@element-plus/icons-vue'

const route = useRoute()

const activeRoute = computed(() => {
  return route.path
})
</script>

<style scoped>
.sidebar {
  width: 200px;
  height: 100vh;
  background-color: #2c3e50;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #1f2d3d;
  border-bottom: 1px solid #1f2d3d;
}

.logo-text {
  color: #fff;
  font-size: 18px;
  font-weight: bold;
}

.sidebar-menu {
  border-right: none;
  width: 100%;
}

.sidebar-menu .el-menu-item {
  height: 56px;
  line-height: 56px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.sidebar-menu .el-menu-item:hover {
  background-color: #263445 !important;
}

.sidebar-menu .el-menu-item.is-active {
  background-color: #263445 !important;
}
</style>

<template>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item :to="{ path: '/dashboard' }">
      <el-icon><HomeFilled /></el-icon>
      <span class="breadcrumb-text">首页</span>
    </el-breadcrumb-item>
    <el-breadcrumb-item v-for="(item, index) in breadcrumbs" :key="index">
      <span class="breadcrumb-text">{{ item.title }}</span>
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { HomeFilled } from '@element-plus/icons-vue'

const route = useRoute()

const breadcrumbs = computed(() => {
  const matched = route.matched.filter(item => item.meta && item.meta.title)
  return matched.map(item => ({
    title: item.meta.title,
    path: item.path
  }))
})
</script>

<style scoped>
.breadcrumb-text {
  margin-left: 4px;
}
</style>

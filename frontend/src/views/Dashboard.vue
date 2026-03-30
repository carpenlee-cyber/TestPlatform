<template>
  <div class="dashboard">
    <h2>仪表盘</h2>
    <div class="stats-container">
      <el-card class="stat-card">
        <template #header>
          <div class="card-header">
            <span>测试用例总数</span>
          </div>
        </template>
        <div class="stat-value">{{ stats.totalTestCases }}</div>
      </el-card>
      <el-card class="stat-card">
        <template #header>
          <div class="card-header">
            <span>已通过</span>
          </div>
        </template>
        <div class="stat-value success">{{ stats.passedTestCases }}</div>
      </el-card>
      <el-card class="stat-card">
        <template #header>
          <div class="card-header">
            <span>缺陷数</span>
          </div>
        </template>
        <div class="stat-value danger">{{ stats.totalBugs }}</div>
      </el-card>
      <el-card class="stat-card">
        <template #header>
          <div class="card-header">
            <span>待修复</span>
          </div>
        </template>
        <div class="stat-value warning">{{ stats.pendingBugs }}</div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as testCaseApi from '../api/testCases'
import * as bugApi from '../api/bugs'

const stats = ref({
  totalTestCases: 0,
  passedTestCases: 0,
  totalBugs: 0,
  pendingBugs: 0
})

const fetchStats = async () => {
  try {
    const res = await testCaseApi.getAll()
    const testCases = res.data || []
    const res2 = await bugApi.getAll()
    const bugs = res2.data || []
    
    stats.value.totalTestCases = testCases.length
    stats.value.passedTestCases = testCases.filter(tc => tc.status === 'PASSED').length
    stats.value.totalBugs = bugs.length
    stats.value.pendingBugs = bugs.filter(bug => bug.status !== 'FIXED').length
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.stat-card {
  text-align: center;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #409eff;
}

.stat-value.success {
  color: #67c23a;
}

.stat-value.danger {
  color: #f56c6c;
}

.stat-value.warning {
  color: #e6a23c;
}

.card-header {
  font-weight: bold;
}
</style>

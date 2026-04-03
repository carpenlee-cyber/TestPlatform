<template>
  <div class="dashboard-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">仪表盘</h1>
        <p class="page-subtitle">欢迎回来，{{ authStore.username }}！这是您今天的测试概览。</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" :icon="Refresh" @click="refreshData" :loading="loading">
          刷新数据
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon blue">
            <el-icon :size="32"><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalTestCases }}</div>
            <div class="stat-label">测试用例总数</div>
          </div>
          <div class="stat-trend">
            <el-tag size="small" type="success">+12%</el-tag>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon green">
            <el-icon :size="32"><CircleCheck /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value success">{{ stats.passedTestCases }}</div>
            <div class="stat-label">已通过用例</div>
          </div>
          <div class="stat-trend">
            <el-tag size="small" type="success">+8%</el-tag>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon red">
            <el-icon :size="32"><Warning /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value danger">{{ stats.totalBugs }}</div>
            <div class="stat-label">缺陷总数</div>
          </div>
          <div class="stat-trend">
            <el-tag size="small" type="danger">+5%</el-tag>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon orange">
            <el-icon :size="32"><Timer /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value warning">{{ stats.pendingBugs }}</div>
            <div class="stat-label">待修复缺陷</div>
          </div>
          <div class="stat-trend">
            <el-tag size="small" type="warning">-2%</el-tag>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-row">
      <el-col :xs="24" :lg="16">
        <el-card class="chart-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>测试趋势</span>
              <el-radio-group v-model="trendPeriod" size="small">
                <el-radio-button label="week">本周</el-radio-button>
                <el-radio-button label="month">本月</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-placeholder">
            <el-empty description="图表组件待集成">
              <template #image>
                <el-icon :size="64" color="#dcdfe6"><TrendCharts /></el-icon>
              </template>
            </el-empty>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="8">
        <el-card class="chart-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>测试状态分布</span>
            </div>
          </template>
          <div class="chart-placeholder">
            <el-empty description="饼图组件待集成">
              <template #image>
                <el-icon :size="64" color="#dcdfe6"><PieChart /></el-icon>
              </template>
            </el-empty>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近活动 -->
    <el-row :gutter="20" class="activity-row">
      <el-col :xs="24">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>最近活动</span>
              <el-link type="primary" :underline="false">查看全部</el-link>
            </div>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="(activity, index) in recentActivities"
              :key="index"
              :type="activity.type"
              :icon="activity.icon"
              :timestamp="activity.time"
            >
              {{ activity.content }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  Refresh,
  Document,
  CircleCheck,
  Warning,
  Timer,
  TrendCharts,
  PieChart,
  Plus,
  Edit,
  Check
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../stores/auth'
import { testCaseApi } from '../api/testCases'
import { bugApi } from '../api/bugs'

const authStore = useAuthStore()
const loading = ref(false)
const trendPeriod = ref('week')

const stats = ref({
  totalTestCases: 0,
  passedTestCases: 0,
  totalBugs: 0,
  pendingBugs: 0
})

const recentActivities = ref([
  {
    content: '创建了新的测试用例 "用户登录功能测试"',
    time: '10分钟前',
    type: 'primary',
    icon: Plus
  },
  {
    content: '更新了缺陷 #123 "首页加载缓慢"',
    time: '30分钟前',
    type: 'warning',
    icon: Edit
  },
  {
    content: '测试用例 "订单提交流程" 已通过',
    time: '1小时前',
    type: 'success',
    icon: Check
  },
  {
    content: '创建了新的缺陷报告 "支付页面样式错乱"',
    time: '2小时前',
    type: 'danger',
    icon: Plus
  }
])

const fetchStats = async () => {
  loading.value = true
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
    ElMessage.error('获取统计数据失败')
  } finally {
    loading.value = false
  }
}

const refreshData = () => {
  fetchStats()
  ElMessage.success('数据已刷新')
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard-page {
  padding-bottom: 20px;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px;
}

.page-subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

/* 统计卡片 */
.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 8px;
  position: relative;
  overflow: hidden;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  flex-shrink: 0;
}

.stat-icon.blue {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.stat-icon.green {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  color: #fff;
}

.stat-icon.red {
  background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
  color: #fff;
}

.stat-icon.orange {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: #fff;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
  line-height: 1.2;
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

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.stat-trend {
  position: absolute;
  top: 16px;
  right: 16px;
}

/* 图表区域 */
.charts-row {
  margin-bottom: 20px;
}

.chart-card {
  height: 400px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.chart-placeholder {
  height: 320px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 响应式 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
  }

  .stats-row .el-col {
    margin-bottom: 16px;
  }

  .chart-card {
    margin-bottom: 16px;
  }
}
</style>

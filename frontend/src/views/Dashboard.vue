<template>
  <div class="dashboard">
    <Header />
    <div class="main-container">
      <Sidebar />
      <div class="content">
        <h1>仪表盘</h1>
        
        <el-row :gutter="20" class="stats-row">
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-icon blue">
                <el-icon><Document /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.testCases }}</div>
                <div class="stat-label">测试用例</div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-icon green">
                <el-icon><CircleCheck /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.passed }}</div>
                <div class="stat-label">已通过</div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-icon red">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.bugs }}</div>
                <div class="stat-label">缺陷</div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-icon orange">
                <el-icon><Timer /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.openBugs }}</div>
                <div class="stat-label">待修复</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <el-row :gutter="20" class="chart-row">
          <el-col :span="12">
            <el-card>
              <template #header>
                <span>测试用例状态分布</span>
              </template>
              <div class="chart-placeholder">
                <div v-for="(count, status) in testCaseStatus" :key="status" class="stat-row">
                  <span :class="['status-dot', status]"></span>
                  <span>{{ status }}: {{ count }}</span>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="12">
            <el-card>
              <template #header>
                <span>缺陷严重性分布</span>
              </template>
              <div class="chart-placeholder">
                <div v-for="(count, severity) in bugSeverity" :key="severity" class="stat-row">
                  <el-tag :type="getSeverityType(severity)">{{ severity }}</el-tag>
                  <span>{{ count }}</span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Document, CircleCheck, Warning, Timer } from '@element-plus/icons-vue'
import Header from '../components/Header.vue'
import Sidebar from '../components/Sidebar.vue'
import { testCaseApi } from '../api/testCases'
import { bugApi } from '../api/bugs'

const stats = ref({
  testCases: 0,
  passed: 0,
  bugs: 0,
  openBugs: 0
})

const testCaseStatus = ref({})
const bugSeverity = ref({})

const getSeverityType = (severity) => {
  const map = { CRITICAL: 'danger', HIGH: 'warning', MEDIUM: 'info', LOW: 'success' }
  return map[severity] || 'info'
}

onMounted(async () => {
  try {
    const [tcRes, bugRes] = await Promise.all([
      testCaseApi.getAll(),
      bugApi.getAll()
    ])
    
    const testCases = tcRes.data
    const bugs = bugRes.data
    
    stats.value.testCases = testCases.length
    stats.value.passed = testCases.filter(tc => tc.status === 'PASSED').length
    stats.value.bugs = bugs.length
    stats.value.openBugs = bugs.filter(b => b.status === 'OPEN').length
    
    testCaseStatus.value = testCases.reduce((acc, tc) => {
      acc[tc.status] = (acc[tc.status] || 0) + 1
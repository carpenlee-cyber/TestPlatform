<template>
  <div class="bugs-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">缺陷管理</h1>
        <p class="page-subtitle">跟踪和管理项目中的缺陷，确保问题及时解决</p>
      </div>
      <el-button type="primary" size="large" @click="handleAdd" :icon="Plus">
        新增Bug
      </el-button>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="filter-card" shadow="never">
      <el-row :gutter="16" align="middle">
        <el-col :xs="24" :sm="8" :md="6">
          <el-input
            v-model="searchQuery"
            placeholder="搜索缺陷标题"
            clearable
            :prefix-icon="Search"
          />
        </el-col>
        <el-col :xs="24" :sm="8" :md="6">
          <el-select v-model="filterSeverity" placeholder="严重性" clearable style="width: 100%">
            <el-option label="严重" value="CRITICAL" />
            <el-option label="高" value="HIGH" />
            <el-option label="中" value="MEDIUM" />
            <el-option label="低" value="LOW" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="8" :md="6">
          <el-select v-model="filterStatus" placeholder="状态" clearable style="width: 100%">
            <el-option label="待处理" value="OPEN" />
            <el-option label="处理中" value="IN_PROGRESS" />
            <el-option label="已解决" value="RESOLVED" />
            <el-option label="已关闭" value="CLOSED" />
          </el-select>
        </el-col>
      </el-row>
    </el-card>

    <!-- 数据表格 -->
    <el-card shadow="hover">
      <el-table 
        :data="paginatedBugs" 
        style="width: 100%" 
        v-loading="loading"
        stripe
        highlight-current-row
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="severity" label="严重性" width="100">
          <template #default="scope">
            <el-tag :type="getSeverityType(scope.row.severity)" effect="light">
              {{ getSeverityLabel(scope.row.severity) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)" effect="light">
              {{ getStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="assignee" label="负责人" width="120" />
        <el-table-column prop="reporter" label="报告人" width="120" />
        <el-table-column prop="createdAt" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.createdAt) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" :icon="Edit" @click="handleEdit(scope.row)">
              编辑
            </el-button>
            <el-popconfirm
              title="确定删除该Bug吗？"
              confirm-button-text="确定"
              cancel-button-text="取消"
              @confirm="handleDelete(scope.row.id)"
            >
              <template #reference>
                <el-button type="danger" size="small" :icon="Delete">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="filteredBugs.length"
          layout="total, sizes, prev, pager, next"
          background
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑Bug' : '新增Bug'"
      width="700px"
      destroy-on-close
    >
      <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="formData.title" placeholder="请输入Bug标题" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="4"
            placeholder="请输入Bug描述，包括复现步骤等"
          />
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="严重性" prop="severity">
              <el-select v-model="formData.severity" placeholder="请选择严重性" style="width: 100%">
                <el-option label="严重" value="CRITICAL" />
                <el-option label="高" value="HIGH" />
                <el-option label="中" value="MEDIUM" />
                <el-option label="低" value="LOW" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="formData.status" placeholder="请选择状态" style="width: 100%">
                <el-option label="待处理" value="OPEN" />
                <el-option label="处理中" value="IN_PROGRESS" />
                <el-option label="已解决" value="RESOLVED" />
                <el-option label="已关闭" value="CLOSED" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="负责人">
              <el-input v-model="formData.assignee" placeholder="请输入负责人" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="报告人">
              <el-input v-model="formData.reporter" placeholder="请输入报告人" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Search, Edit, Delete } from '@element-plus/icons-vue'
import { bugApi } from '../api/bugs'

// 数据
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const bugList = ref([])

// 搜索和筛选
const searchQuery = ref('')
const filterSeverity = ref('')
const filterStatus = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(10)

const formData = reactive({
  id: null,
  title: '',
  description: '',
  severity: 'MEDIUM',
  status: 'OPEN',
  assignee: '',
  reporter: ''
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  severity: [{ required: true, message: '请选择严重性', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

const getSeverityType = (severity) => {
  const types = {
    CRITICAL: 'danger',
    HIGH: 'warning',
    MEDIUM: '',
    LOW: 'info'
  }
  return types[severity] || ''
}

const getSeverityLabel = (severity) => {
  const labels = {
    CRITICAL: '严重',
    HIGH: '高',
    MEDIUM: '中',
    LOW: '低'
  }
  return labels[severity] || severity
}

const getStatusType = (status) => {
  const types = {
    OPEN: 'danger',
    IN_PROGRESS: 'warning',
    RESOLVED: 'success',
    CLOSED: 'info'
  }
  return types[status] || ''
}

const getStatusLabel = (status) => {
  const labels = {
    OPEN: '待处理',
    IN_PROGRESS: '处理中',
    RESOLVED: '已解决',
    CLOSED: '已关闭'
  }
  return labels[status] || status
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}

// 筛选后的数据
const filteredBugs = computed(() => {
  let result = bugList.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(bug => 
      bug.title?.toLowerCase().includes(query) ||
      bug.description?.toLowerCase().includes(query)
    )
  }

  if (filterSeverity.value) {
    result = result.filter(bug => bug.severity === filterSeverity.value)
  }

  if (filterStatus.value) {
    result = result.filter(bug => bug.status === filterStatus.value)
  }

  return result
})

// 分页后的数据
const paginatedBugs = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredBugs.value.slice(start, end)
})

const loadBugList = async () => {
  loading.value = true
  try {
    const res = await bugApi.getAll()
    bugList.value = res.data || []
  } catch (error) {
    ElMessage.error('加载Bug列表失败')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  formData.id = null
  formData.title = ''
  formData.description = ''
  formData.severity = 'MEDIUM'
  formData.status = 'OPEN'
  formData.assignee = ''
  formData.reporter = ''
}

const handleAdd = () => {
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  Object.assign(formData, row)
  dialogVisible.value = true
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    if (isEdit.value) {
      await bugApi.update(formData.id, formData)
      ElMessage.success('更新成功')
    } else {
      await bugApi.create(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadBugList()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (id) => {
  try {
    await bugApi.delete(id)
    ElMessage.success('删除成功')
    loadBugList()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  loadBugList()
})
</script>

<style scoped>
.bugs-page {
  padding-bottom: 20px;
}

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

.filter-card {
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
  }
}
</style>

<template>
  <div class="test-cases-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">测试用例管理</h1>
        <p class="page-subtitle">管理您的测试用例，确保软件质量</p>
      </div>
      <el-button type="primary" size="large" @click="openDialog()" :icon="Plus">
        新建用例
      </el-button>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="filter-card" shadow="never">
      <el-row :gutter="16" align="middle">
        <el-col :xs="24" :sm="8" :md="6">
          <el-input
            v-model="searchQuery"
            placeholder="搜索测试用例"
            clearable
            :prefix-icon="Search"
          />
        </el-col>
        <el-col :xs="24" :sm="8" :md="6">
          <el-select v-model="filterPriority" placeholder="优先级" clearable style="width: 100%">
            <el-option label="高" value="HIGH" />
            <el-option label="中" value="MEDIUM" />
            <el-option label="低" value="LOW" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="8" :md="6">
          <el-select v-model="filterStatus" placeholder="状态" clearable style="width: 100%">
            <el-option label="草稿" value="DRAFT" />
            <el-option label="就绪" value="READY" />
            <el-option label="通过" value="PASSED" />
            <el-option label="失败" value="FAILED" />
          </el-select>
        </el-col>
      </el-row>
    </el-card>

    <!-- 数据表格 -->
    <el-card shadow="hover">
      <el-table 
        :data="filteredTestCases" 
        v-loading="loading" 
        stripe
        highlight-current-row
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="{ row }">
            <el-tag :type="getPriorityType(row.priority)" effect="light">
              {{ getPriorityLabel(row.priority) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" effect="light">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="assignee" label="负责人" width="120" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" :icon="Edit" @click="openDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" :icon="Delete" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="filteredTestCases.length"
          layout="total, sizes, prev, pager, next"
          background
        />
      </div>
    </el-card>

    <!-- 编辑/新建对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="isEdit ? '编辑测试用例' : '新建测试用例'" 
      width="700px"
      destroy-on-close
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入测试用例标题" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input 
            v-model="form.description" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入测试用例描述"
          />
        </el-form-item>
        <el-form-item label="步骤" prop="steps">
          <el-input 
            v-model="form.steps" 
            type="textarea" 
            :rows="4" 
            placeholder="请输入测试步骤，每行一个步骤"
          />
        </el-form-item>
        <el-form-item label="预期结果" prop="expectedResult">
          <el-input 
            v-model="form.expectedResult" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入预期结果"
          />
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="优先级" prop="priority">
              <el-select v-model="form.priority" style="width: 100%">
                <el-option label="高" value="HIGH" />
                <el-option label="中" value="MEDIUM" />
                <el-option label="低" value="LOW" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="form.status" style="width: 100%">
                <el-option label="草稿" value="DRAFT" />
                <el-option label="就绪" value="READY" />
                <el-option label="通过" value="PASSED" />
                <el-option label="失败" value="FAILED" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="负责人" prop="assignee">
          <el-input v-model="form.assignee" placeholder="请输入负责人姓名" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from 'vue'
import { Plus, Search, Edit, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { testCaseApi } from '../api/testCases'

// 数据
const testCases = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const formRef = ref()

// 搜索和筛选
const searchQuery = ref('')
const filterPriority = ref('')
const filterStatus = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(10)

const form = reactive({
  id: null,
  title: '',
  description: '',
  steps: '',
  expectedResult: '',
  priority: 'MEDIUM',
  status: 'DRAFT',
  assignee: ''
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  priority: [{ required: true, message: '请选择优先级', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

// 筛选后的数据
const filteredTestCases = computed(() => {
  let result = testCases.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(tc => 
      tc.title?.toLowerCase().includes(query) ||
      tc.description?.toLowerCase().includes(query)
    )
  }

  if (filterPriority.value) {
    result = result.filter(tc => tc.priority === filterPriority.value)
  }

  if (filterStatus.value) {
    result = result.filter(tc => tc.status === filterStatus.value)
  }

  return result
})

const loadTestCases = async () => {
  loading.value = true
  try {
    const res = await testCaseApi.getAll()
    testCases.value = res.data || []
  } catch (error) {
    ElMessage.error('加载测试用例失败')
  } finally {
    loading.value = false
  }
}

const openDialog = (row = null) => {
  isEdit.value = !!row
  if (row) {
    Object.assign(form, row)
  } else {
    Object.assign(form, { 
      id: null, 
      title: '', 
      description: '', 
      steps: '', 
      expectedResult: '', 
      priority: 'MEDIUM', 
      status: 'DRAFT', 
      assignee: '' 
    })
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
  } catch {
    return
  }

  submitting.value = true
  try {
    if (isEdit.value) {
      await testCaseApi.update(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await testCaseApi.create(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadTestCases()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该测试用例吗？', '提示', { type: 'warning' })
    await testCaseApi.delete(row.id)
    ElMessage.success('删除成功')
    loadTestCases()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const getPriorityType = (p) => ({ HIGH: 'danger', MEDIUM: 'warning', LOW: 'info' }[p] || 'info')
const getPriorityLabel = (p) => ({ HIGH: '高', MEDIUM: '中', LOW: '低' }[p] || p)
const getStatusType = (s) => ({ PASSED: 'success', FAILED: 'danger', DRAFT: 'info', READY: 'primary' }[s] || 'info')
const getStatusLabel = (s) => ({ PASSED: '通过', FAILED: '失败', DRAFT: '草稿', READY: '就绪' }[s] || s)

onMounted(loadTestCases)
</script>

<style scoped>
.test-cases-page {
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

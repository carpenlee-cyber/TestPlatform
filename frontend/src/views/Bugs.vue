<template>
  <div class="bugs-page">
    <Header />
    <Sidebar />
    <div class="main-content">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>缺陷管理</span>
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>
              新增Bug
            </el-button>
          </div>
        </template>
        
        <el-table :data="bugList" style="width: 100%" v-loading="loading">
          <el-table-column prop="title" label="标题" min-width="200" />
          <el-table-column prop="severity" label="严重性" width="120">
            <template #default="scope">
              <el-tag :type="getSeverityType(scope.row.severity)">
                {{ scope.row.severity }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="120">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ scope.row.status }}
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
              <el-button type="primary" size="small" @click="handleEdit(scope.row)">
                编辑
              </el-button>
              <el-popconfirm
                title="确定删除该Bug吗？"
                confirm-button-text="确定"
                cancel-button-text="取消"
                @confirm="handleDelete(scope.row.id)"
              >
                <template #reference>
                  <el-button type="danger" size="small">删除</el-button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
    
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑Bug' : '新增Bug'"
      width="600px"
      destroy-on-close
    >
      <el-form ref="formRef" :model="formData" :rules="rules" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="formData.title" placeholder="请输入Bug标题" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            rows="4"
            placeholder="请输入Bug描述"
          />
        </el-form-item>
        <el-form-item label="严重性" prop="severity">
          <el-select v-model="formData.severity" placeholder="请选择严重性">
            <el-option label="CRITICAL" value="CRITICAL" />
            <el-option label="HIGH" value="HIGH" />
            <el-option label="MEDIUM" value="MEDIUM" />
            <el-option label="LOW" value="LOW" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="formData.status" placeholder="请选择状态">
            <el-option label="OPEN" value="OPEN" />
            <el-option label="IN_PROGRESS" value="IN_PROGRESS" />
            <el-option label="RESOLVED" value="RESOLVED" />
            <el-option label="CLOSED" value="CLOSED" />
          </el-select>
        </el-form-item>
        <el-form-item label="负责人">
          <el-input v-model="formData.assignee" placeholder="请输入负责人" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import Header from '../components/Header.vue'
import Sidebar from '../components/Sidebar.vue'
import { bugApi } from '../api/bugs'

const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

const bugList = ref([])

const formData = reactive({
  id: null,
  title: '',
  description: '',
  severity: 'MEDIUM',
  status: 'OPEN',
  assignee: ''
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

const getStatusType = (status) => {
  const types = {
    OPEN: 'primary',
    IN_PROGRESS: 'warning',
    RESOLVED: 'success',
    CLOSED: 'info'
  }
  return types[status] || ''
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}

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
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  margin-left: 200px;
  margin-top: 60px;
  padding: 20px;
  min-height: calc(100vh - 60px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

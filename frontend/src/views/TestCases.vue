<template>
  <div class="test-cases">
    <Header />
    <div class="main-container">
      <Sidebar />
      <div class="content">
        <div class="page-header">
          <h1>测试用例管理</h1>
          <el-button type="primary" @click="openDialog()">
            <el-icon><Plus /></el-icon> 新建用例
          </el-button>
        </div>
        
        <el-card>
          <el-table :data="testCases" v-loading="loading" stripe>
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="title" label="标题" min-width="200" />
            <el-table-column prop="priority" label="优先级" width="100">
              <template #default="{ row }">
                <el-tag :type="getPriorityType(row.priority)">{{ row.priority }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="assignee" label="负责人" width="120" />
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="openDialog(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        
        <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑测试用例' : '新建测试用例'" width="600px">
          <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
            <el-form-item label="标题" prop="title">
              <el-input v-model="form.title" />
            </el-form-item>
            <el-form-item label="描述" prop="description">
              <el-input v-model="form.description" type="textarea" :rows="3" />
            </el-form-item>
            <el-form-item label="步骤" prop="steps">
              <el-input v-model="form.steps" type="textarea" :rows="4" />
            </el-form-item>
            <el-form-item label="预期结果" prop="expectedResult">
              <el-input v-model="form.expectedResult" type="textarea" :rows="3" />
            </el-form-item>
            <el-form-item label="优先级" prop="priority">
              <el-select v-model="form.priority" style="width: 100%">
                <el-option label="高" value="HIGH" />
                <el-option label="中" value="MEDIUM" />
                <el-option label="低" value="LOW" />
              </el-select>
            </el-form-item>
            <el-form-item label="状态" prop="status">
              <el-select v-model="form.status" style="width: 100%">
                <el-option label="草稿" value="DRAFT" />
                <el-option label="就绪" value="READY" />
                <el-option label="通过" value="PASSED" />
                <el-option label="失败" value="FAILED" />
              </el-select>
            </el-form-item>
            <el-form-item label="负责人" prop="assignee">
              <el-input v-model="form.assignee" />
            </el-form-item>
          </el-form>
          <template #footer>
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
          </template>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import Header from '../components/Header.vue'
import Sidebar from '../components/Sidebar.vue'
import { testCaseApi } from '../api/testCases'

const testCases = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const formRef = ref()

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
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }]
}

const loadTestCases = async () => {
  loading.value = true
  try {
    const res = await testCaseApi.getAll()
    testCases.value = res.data
  } finally {
    loading.value = false
  }
}

const openDialog = (row = null) => {
  isEdit.value = !!row
  if (row) {
    Object.assign(form, row)
  } else {
    Object.assign(form, { id: null, title: '', description: '', steps: '', expectedResult: '', priority: 'MEDIUM', status: 'DRAFT', assignee: '' })
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  await formRef.value.validate()
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
    if (error !== 'cancel') ElMessage.error('删除失败')
  }
}

const getPriorityType = (p) => ({ HIGH: 'danger', MEDIUM: 'warning', LOW: 'info' }[p] || 'info')
const getStatusType = (s) => ({ PASSED: 'success', FAILED: 'danger', DRAFT: 'info', READY: 'primary' }[s] || 'info')

onMounted(loadTestCases)
</script>

<style scoped>
.test-cases { min-height: 100vh; background: #f5f7fa; }
.main-container { display: flex; }
.content { flex: 1; padding: 20px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
</style>

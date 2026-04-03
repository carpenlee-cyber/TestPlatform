<template>
  <div class="login-page">
    <!-- 左侧品牌区域 -->
    <div class="login-brand">
      <div class="brand-content">
        <div class="brand-logo">
          <el-icon :size="64" color="#fff"><Platform /></el-icon>
        </div>
        <h1 class="brand-title">TestPlatform</h1>
        <p class="brand-slogan">专业的测试管理平台</p>
        <div class="brand-features">
          <div class="feature-item">
            <el-icon :size="20" color="#67c23a"><CircleCheck /></el-icon>
            <span>测试用例管理</span>
          </div>
          <div class="feature-item">
            <el-icon :size="20" color="#67c23a"><CircleCheck /></el-icon>
            <span>缺陷追踪系统</span>
          </div>
          <div class="feature-item">
            <el-icon :size="20" color="#67c23a"><CircleCheck /></el-icon>
            <span>实时数据统计</span>
          </div>
        </div>
      </div>
      <div class="brand-footer">
        <p>© 2024 TestPlatform. All rights reserved.</p>
      </div>
    </div>

    <!-- 右侧登录区域 -->
    <div class="login-form-section">
      <div class="form-container">
        <div class="form-header">
          <h2 class="form-title">欢迎回来</h2>
          <p class="form-subtitle">请登录您的账户以继续</p>
        </div>

        <el-form
          :model="form"
          :rules="rules"
          ref="formRef"
          class="login-form"
          @keyup.enter="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
              size="large"
              :prefix-icon="User"
              clearable
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              :prefix-icon="Lock"
              show-password
              clearable
            />
          </el-form-item>

          <div class="form-options">
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
            <el-link type="primary" :underline="false">忘记密码?</el-link>
          </div>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              @click="handleLogin"
              class="login-btn"
            >
              登 录
            </el-button>
          </el-form-item>

          <el-divider>
            <span class="divider-text">或</span>
          </el-divider>

          <el-form-item>
            <el-button
              size="large"
              @click="handleRegister"
              :loading="registerLoading"
              class="register-btn"
            >
              创建新账户
            </el-button>
          </el-form-item>
        </el-form>

        <div class="form-footer">
          <p>登录即表示您同意我们的 <el-link type="primary">服务条款</el-link> 和 <el-link type="primary">隐私政策</el-link></p>
        </div>
      </div>
    </div>

    <!-- 注册对话框 -->
    <el-dialog
      v-model="registerDialogVisible"
      title="创建新账户"
      width="420px"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <el-form
        :model="registerForm"
        :rules="registerRules"
        ref="registerFormRef"
        label-position="top"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名"
            :prefix-icon="User"
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="registerDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="registerLoading" @click="submitRegister">
          注册
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock, Platform, CircleCheck } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../stores/auth'
import { authApi } from '../api/auth'

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref()
const registerFormRef = ref()
const loading = ref(false)
const registerLoading = ref(false)
const rememberMe = ref(false)
const registerDialogVisible = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: ''
})

// 自定义密码确认校验
const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应为 3-20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应为 6-20 个字符', trigger: 'blur' }
  ]
}

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应为 3-20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应为 6-20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  try {
    await formRef.value.validate()
  } catch (error) {
    return
  }

  loading.value = true

  try {
    const res = await authApi.login({
      username: form.username,
      password: form.password
    })

    authStore.setAuth(res.data.token, {
      username: res.data.username,
      role: res.data.role
    }, rememberMe.value)

    ElMessage.success({
      message: '登录成功，欢迎回来！',
      duration: 2000
    })

    router.push('/dashboard')
  } catch (error) {
    const errorMsg = error.response?.data?.message || error.response?.data || '登录失败，请检查用户名和密码'
    ElMessage.error({
      message: errorMsg,
      duration: 3000
    })
  } finally {
    loading.value = false
  }
}

const handleRegister = () => {
  registerDialogVisible.value = true
}

const submitRegister = async () => {
  try {
    await registerFormRef.value.validate()
  } catch (error) {
    return
  }

  registerLoading.value = true

  try {
    await authApi.register({
      username: registerForm.username,
      password: registerForm.password
    })

    ElMessage.success({
      message: '注册成功，请使用新账户登录',
      duration: 2000
    })

    registerDialogVisible.value = false
    // 自动填充用户名
    form.username = registerForm.username
    registerForm.username = ''
    registerForm.password = ''
    registerForm.confirmPassword = ''
  } catch (error) {
    const errorMsg = error.response?.data?.message || error.response?.data || '注册失败，请稍后重试'
    ElMessage.error({
      message: errorMsg,
      duration: 3000
    })
  } finally {
    registerLoading.value = false
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

/* 左侧品牌区域 */
.login-brand {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 60px;
  position: relative;
  color: #fff;
}

.brand-content {
  text-align: center;
  max-width: 400px;
}

.brand-logo {
  margin-bottom: 24px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.brand-title {
  font-size: 42px;
  font-weight: 700;
  margin: 0 0 12px;
  letter-spacing: -1px;
}

.brand-slogan {
  font-size: 18px;
  opacity: 0.9;
  margin: 0 0 48px;
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: flex-start;
  margin: 0 auto;
  width: fit-content;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;
}

.brand-footer {
  position: absolute;
  bottom: 24px;
  font-size: 14px;
  opacity: 0.7;
}

/* 右侧登录区域 */
.login-form-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f7fa;
  padding: 40px;
}

.form-container {
  width: 100%;
  max-width: 400px;
  background: #fff;
  padding: 48px;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
}

.form-header {
  text-align: center;
  margin-bottom: 32px;
}

.form-title {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px;
}

.form-subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.login-form {
  :deep(.el-input__wrapper) {
    border-radius: 8px;
    padding: 4px 12px;
  }

  :deep(.el-input__inner) {
    height: 44px;
  }
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.login-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 8px;
}

.register-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  border-radius: 8px;
}

.divider-text {
  color: #909399;
  font-size: 12px;
}

.form-footer {
  margin-top: 24px;
  text-align: center;
  font-size: 12px;
  color: #909399;
  line-height: 1.6;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .login-brand {
    display: none;
  }

  .login-form-section {
    padding: 20px;
  }

  .form-container {
    padding: 32px 24px;
  }
}

@media (max-width: 480px) {
  .form-container {
    padding: 24px 20px;
    border-radius: 12px;
  }

  .form-title {
    font-size: 24px;
  }
}
</style>

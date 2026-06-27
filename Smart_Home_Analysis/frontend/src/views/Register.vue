<template>
  <div class="register-split">
    <!-- Left: decorative PixelBlast zone -->
    <div class="register-decor">
      <PixelBlast
        variant="circle"
        :pixelSize="10"
        color="#cc785c"
        :patternScale="3"
        :patternDensity="1.8"
        :pixelSizeJitter="0.3"
        :enableRipples="true"
        :rippleSpeed="0.4"
        :rippleThickness="0.14"
        :rippleIntensityScale="1.5"
        :liquid="true"
        :liquidStrength="0.12"
        :liquidRadius="1.2"
        :liquidWobbleSpeed="5"
        :speed="0.6"
        :edgeFade="0.1"
        :transparent="true"
      />
      <div class="decor-overlay">
        <div class="decor-content">
          <h1 class="decor-title">Join Us</h1>
          <p class="decor-tagline">智能家居销量数据分析系统</p>
          <div class="decor-line"></div>
          <p class="decor-desc">创建您的账户，开启数据驱动的智能决策之旅</p>
        </div>
      </div>
    </div>

    <!-- Right: register card -->
    <div class="register-panel">
      <div class="register-wrapper">
        <el-card class="register-card" shadow="never">
          <template #header>
            <div class="card-header">
              <h2>创建账户</h2>
              <p class="subtitle">注册新账户以使用系统</p>
            </div>
          </template>
          <el-form :model="registerForm" :rules="registerRules" ref="registerFormRef" class="register-form">
            <el-form-item prop="username">
              <el-input
                v-model="registerForm.username"
                placeholder="请输入用户名"
                size="large"
                :prefix-icon="User"
              />
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                v-model="registerForm.password"
                type="password"
                placeholder="请输入密码（至少6位）"
                show-password
                size="large"
                :prefix-icon="Lock"
              />
            </el-form-item>
            <el-form-item prop="confirmPassword">
              <el-input
                v-model="registerForm.confirmPassword"
                type="password"
                placeholder="请再次输入密码"
                show-password
                size="large"
                :prefix-icon="Lock"
              />
            </el-form-item>
            <el-form-item prop="email">
              <el-input
                v-model="registerForm.email"
                placeholder="请输入邮箱（可选）"
                size="large"
                :prefix-icon="Message"
              />
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                @click="handleRegister"
                :loading="loading"
                size="large"
                class="register-btn"
              >
                注 册
              </el-button>
            </el-form-item>
            <el-form-item>
              <div class="register-footer">
                <span>已有账号？</span>
                <el-link type="primary" @click="goToLogin">立即登录</el-link>
              </div>
            </el-form-item>
          </el-form>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message } from '@element-plus/icons-vue'
import request from '../utils/request'
import PixelBlast from '../components/PixelBlast.vue'

export default {
  name: 'Register',
  components: { User, Lock, Message, PixelBlast },
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const registerFormRef = ref(null)

    const registerForm = reactive({
      username: '',
      password: '',
      confirmPassword: '',
      email: ''
    })

    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== registerForm.password) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }

    const registerRules = {
      username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
      ],
      confirmPassword: [{ required: true, validator: validateConfirmPassword, trigger: 'blur' }]
    }

    const handleRegister = async () => {
      if (!registerFormRef.value) return

      await registerFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            const { confirmPassword, ...registerData } = registerForm
            const response = await request.post('/auth/register', registerData)
            if (response.code === 200) {
              ElMessage.success('注册成功，请登录')
              router.push('/login')
            } else {
              ElMessage.error(response.message || '注册失败')
            }
          } catch (error) {
            ElMessage.error('注册失败: ' + (error.response?.data?.message || error.message))
          } finally {
            loading.value = false
          }
        }
      })
    }

    const goToLogin = () => {
      router.push('/login')
    }

    return {
      registerForm,
      registerRules,
      registerFormRef,
      loading,
      handleRegister,
      goToLogin
    }
  }
}
</script>

<style scoped>
.register-split {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background-color: #faf9f5;
}

/* ---- Left decorative zone ---- */
.register-decor {
  flex: 0 0 55%;
  position: relative;
  overflow: hidden;
  background-color: #faf9f5;
}

.decor-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  z-index: 2;
}

.decor-content {
  text-align: center;
  padding: 48px;
}

.decor-title {
  margin: 0 0 8px 0;
  font-family: 'Cormorant Garamond', 'EB Garamond', 'Times New Roman', serif;
  font-size: 56px;
  font-weight: 400;
  letter-spacing: -1px;
  color: #141413;
  line-height: 1.1;
}

.decor-tagline {
  margin: 0 0 32px 0;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: #8e8b82;
}

.decor-line {
  width: 60px;
  height: 1px;
  background-color: #cc785c;
  margin: 0 auto 32px;
}

.decor-desc {
  margin: 0;
  font-family: 'Inter', sans-serif;
  font-size: 15px;
  font-weight: 400;
  color: #8e8b82;
  line-height: 1.6;
  max-width: 320px;
}

/* ---- Right panel ---- */
.register-panel {
  flex: 0 0 45%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
  background-color: #faf9f5;
}

.register-wrapper {
  width: 100%;
  max-width: 420px;
}

.register-card {
  background-color: #faf9f5;
  border: 1px solid #e6dfd8;
  border-radius: 12px;
}

.register-card :deep(.el-card__header) {
  padding: 32px 36px 0 36px;
  border-bottom: none;
}

.register-card :deep(.el-card__body) {
  padding: 24px 36px 36px 36px;
}

.card-header {
  text-align: left;
}

.card-header h2 {
  margin: 0 0 6px 0;
  color: #141413;
  font-family: 'Cormorant Garamond', 'EB Garamond', 'Times New Roman', serif;
  font-size: 32px;
  font-weight: 400;
  letter-spacing: -0.3px;
}

.subtitle {
  margin: 0;
  color: #8e8b82;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 400;
}

.register-form {
  margin-top: 4px;
}

:deep(.el-form-item) {
  margin-bottom: 18px;
}

:deep(.el-form-item__label) {
  display: none;
}

.register-form :deep(.el-input__wrapper) {
  height: 44px;
  background-color: #faf9f5;
  border-radius: 8px;
  box-shadow: 0 0 0 1px #e6dfd8 inset;
  padding: 0 14px;
  transition: box-shadow 0.2s ease;
}

.register-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #8e8b82 inset;
}

.register-form :deep(.el-input.is-focus .el-input__wrapper) {
  box-shadow: 0 0 0 1px #cc785c inset, 0 0 0 3px rgba(204, 120, 92, 0.12);
}

.register-btn {
  width: 100%;
}

.register-form :deep(.el-button--primary) {
  width: 100%;
  height: 44px;
  background-color: #cc785c;
  border: none;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 500;
  border-radius: 8px;
  letter-spacing: 1px;
}

.register-form :deep(.el-button--primary:hover) {
  background-color: #a9583e;
}

.register-footer {
  width: 100%;
  text-align: center;
  color: #6c6a64;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
}

.register-footer :deep(.el-link) {
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 500;
}

.register-footer :deep(.el-link--inner) {
  color: #cc785c;
}

/* ---- Responsive ---- */
@media (max-width: 768px) {
  .register-decor {
    display: none;
  }

  .register-panel {
    flex: 1 1 100%;
    padding: 24px;
  }

  .register-card :deep(.el-card__header) {
    padding: 28px 24px 0 24px;
  }

  .register-card :deep(.el-card__body) {
    padding: 20px 24px;
  }
}
</style>

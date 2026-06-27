<template>
  <div class="auth-split">
    <!-- Left: decorative PixelBlast zone — never changes -->
    <div class="auth-decor">
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
          <h1 class="decor-title">Smart Home</h1>
          <p class="decor-tagline">智能家居销量数据分析系统</p>
          <div class="decor-line"></div>
          <p class="decor-desc">数据驱动的智能决策，让每一笔销售都有据可依</p>
        </div>
      </div>
    </div>

    <!-- Right: form cards toggle via route -->
    <div class="auth-panel">
      <div class="auth-wrapper">
        <Transition name="card-swap" mode="out-in">
          <!-- ========== LOGIN CARD ========== -->
          <el-card v-if="isLogin" key="login" class="auth-card" shadow="never">
            <template #header>
              <div class="card-header">
                <h2>欢迎回来</h2>
                <p class="subtitle">登录您的账户以继续</p>
              </div>
            </template>
            <el-form
              :model="loginForm"
              :rules="loginRules"
              ref="loginFormRef"
              class="auth-form"
              @keyup.enter="handleLogin"
            >
              <el-form-item prop="username">
                <el-input
                  v-model="loginForm.username"
                  placeholder="请输入用户名"
                  size="large"
                  :prefix-icon="User"
                  @keyup.enter="handleLogin"
                />
              </el-form-item>
              <el-form-item prop="password">
                <el-input
                  v-model="loginForm.password"
                  type="password"
                  placeholder="请输入密码"
                  show-password
                  size="large"
                  :prefix-icon="Lock"
                  @keyup.enter="handleLogin"
                />
              </el-form-item>
              <el-form-item>
                <el-button
                  type="primary"
                  @click="handleLogin"
                  :loading="loginLoading"
                  size="large"
                  class="auth-btn"
                >
                  登 录
                </el-button>
              </el-form-item>
              <el-form-item>
                <div class="auth-footer">
                  <span>还没有账号？</span>
                  <el-link type="primary" @click="switchToRegister">立即注册</el-link>
                </div>
              </el-form-item>
            </el-form>
          </el-card>

          <!-- ========== REGISTER CARD ========== -->
          <el-card v-else key="register" class="auth-card" shadow="never">
            <template #header>
              <div class="card-header">
                <h2>创建账户</h2>
                <p class="subtitle">注册新账户以使用系统</p>
              </div>
            </template>
            <el-form
              :model="registerForm"
              :rules="registerRules"
              ref="registerFormRef"
              class="auth-form"
              @keyup.enter="handleRegister"
            >
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
                  :loading="registerLoading"
                  size="large"
                  class="auth-btn"
                >
                  注 册
                </el-button>
              </el-form-item>
              <el-form-item>
                <div class="auth-footer">
                  <span>已有账号？</span>
                  <el-link type="primary" @click="switchToLogin">立即登录</el-link>
                </div>
              </el-form-item>
            </el-form>
          </el-card>
        </Transition>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message } from '@element-plus/icons-vue'
import request from '../utils/request'
import PixelBlast from '../components/PixelBlast.vue'

export default {
  name: 'AuthPage',
  components: { User, Lock, Message, PixelBlast },
  setup() {
    const router = useRouter()
    const route = useRoute()

    const isLogin = computed(() => route.path === '/login')

    // ---- Login state ----
    const loginLoading = ref(false)
    const loginFormRef = ref(null)
    const loginForm = reactive({ username: '', password: '' })
    const loginRules = {
      username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
      password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
    }

    // ---- Register state ----
    const registerLoading = ref(false)
    const registerFormRef = ref(null)
    const registerForm = reactive({ username: '', password: '', confirmPassword: '', email: '' })
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== registerForm.password) { callback(new Error('两次输入密码不一致')) }
      else { callback() }
    }
    const registerRules = {
      username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
      ],
      confirmPassword: [{ required: true, validator: validateConfirmPassword, trigger: 'blur' }]
    }

    // ---- Toggle between forms (left panel stays unchanged) ----
    const switchToRegister = () => { router.push('/register') }
    const switchToLogin = () => { router.push('/login') }

    // ---- Login handler ----
    const handleLogin = async () => {
      if (!loginFormRef.value) return
      await loginFormRef.value.validate(async (valid) => {
        if (valid) {
          loginLoading.value = true
          try {
            const response = await request.post('/auth/login', loginForm)
            if (response.code === 200) {
              const userInfo = response.data.user
              localStorage.setItem('userInfo', JSON.stringify(userInfo))
              localStorage.setItem('token', 'token_' + Date.now())
              ElMessage.success('登录成功')
              router.push(userInfo.role === 'admin' ? '/data-management' : '/visualization/sales-trend')
            } else {
              ElMessage.error(response.message || '登录失败')
            }
          } catch (error) {
            ElMessage.error('登录失败: ' + (error.response?.data?.message || error.message))
          } finally {
            loginLoading.value = false
          }
        }
      })
    }

    // ---- Register handler ----
    const handleRegister = async () => {
      if (!registerFormRef.value) return
      await registerFormRef.value.validate(async (valid) => {
        if (valid) {
          registerLoading.value = true
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
            registerLoading.value = false
          }
        }
      })
    }

    return {
      isLogin,
      loginLoading, loginForm, loginRules, loginFormRef,
      registerLoading, registerForm, registerRules, registerFormRef,
      switchToRegister, switchToLogin,
      handleLogin, handleRegister
    }
  }
}
</script>

<style scoped>
.auth-split {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background-color: #faf9f5;
}

/* ---- Left decorative zone —– */
.auth-decor {
  flex: 0 0 58%;
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

.decor-content { text-align: center; padding: 48px; }

.decor-title {
  margin: 0 0 8px 0;
  font-family: 'Cormorant Garamond', 'EB Garamond', 'Times New Roman', serif;
  font-size: 64px; font-weight: 400; letter-spacing: -1px; color: #141413; line-height: 1.1;
}

.decor-tagline {
  margin: 0 0 32px 0;
  font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 500;
  letter-spacing: 3px; text-transform: uppercase; color: #8e8b82;
}

.decor-line { width: 60px; height: 1px; background-color: #cc785c; margin: 0 auto 32px; }

.decor-desc {
  margin: 0; font-family: 'Inter', sans-serif; font-size: 15px; font-weight: 400;
  color: #8e8b82; line-height: 1.6; max-width: 320px;
}

/* ---- Right panel ---- */
.auth-panel {
  flex: 0 0 42%;
  display: flex; align-items: center; justify-content: center;
  padding: 48px; background-color: #faf9f5;
}

.auth-wrapper { width: 100%; max-width: 400px; }

.auth-card {
  background-color: #faf9f5; border: 1px solid #e6dfd8; border-radius: 12px;
}

.auth-card :deep(.el-card__header) { padding: 40px 40px 0 40px; border-bottom: none; }
.auth-card :deep(.el-card__body) { padding: 32px 40px 40px 40px; }

.card-header { text-align: left; }

.card-header h2 {
  margin: 0 0 6px 0; color: #141413;
  font-family: 'Cormorant Garamond', 'EB Garamond', 'Times New Roman', serif;
  font-size: 32px; font-weight: 400; letter-spacing: -0.3px;
}

.subtitle {
  margin: 0; color: #8e8b82; font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 400;
}

.auth-form { margin-top: 8px; }

:deep(.el-form-item) { margin-bottom: 20px; }
:deep(.el-form-item__label) { display: none; }

.auth-form :deep(.el-input__wrapper) {
  height: 46px; background-color: #faf9f5; border-radius: 8px;
  box-shadow: 0 0 0 1px #e6dfd8 inset; padding: 0 14px; transition: box-shadow 0.2s ease;
}
.auth-form :deep(.el-input__wrapper:hover) { box-shadow: 0 0 0 1px #8e8b82 inset; }
.auth-form :deep(.el-input.is-focus .el-input__wrapper) {
  box-shadow: 0 0 0 1px #cc785c inset, 0 0 0 3px rgba(204, 120, 92, 0.12);
}

.auth-btn { width: 100%; }

.auth-form :deep(.el-button--primary) {
  width: 100%; height: 46px; background-color: #cc785c; border: none;
  font-family: 'Inter', sans-serif; font-size: 15px; font-weight: 500;
  border-radius: 8px; letter-spacing: 1px;
}
.auth-form :deep(.el-button--primary:hover) { background-color: #a9583e; }

.auth-footer {
  width: 100%; text-align: center; color: #6c6a64; font-family: 'Inter', sans-serif; font-size: 14px;
}
.auth-footer :deep(.el-link) { font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 500; }
.auth-footer :deep(.el-link--inner) { color: #cc785c; }

/* ---- Card swap transition ---- */
.card-swap-enter-active,
.card-swap-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.card-swap-enter-from { opacity: 0; transform: translateY(12px); }
.card-swap-leave-to { opacity: 0; transform: translateY(-12px); }

/* ---- Responsive ---- */
@media (max-width: 768px) {
  .auth-decor { display: none; }
  .auth-panel { flex: 1 1 100%; padding: 24px; }
  .auth-card :deep(.el-card__header) { padding: 32px 24px 0 24px; }
  .auth-card :deep(.el-card__body) { padding: 24px; }
}
</style>

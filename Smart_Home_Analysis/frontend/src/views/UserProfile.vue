<template>
  <div class="user-profile">
    <el-card shadow="never" class="main-card">
      <template #header>
        <div class="card-header">
          <h3>个人信息</h3>
          <p class="subtitle">修改您的个人信息，用户名不可修改</p>
        </div>
      </template>
      
      <el-form
        :model="formData"
        label-width="120px"
        :rules="formRules"
        ref="formRef"
        class="profile-form"
      >
        <el-form-item label="用户名">
          <el-input 
            v-model="formData.username" 
            disabled
            size="large"
          />
          <span class="form-tip">用户名不可修改</span>
        </el-form-item>
        
        <el-form-item label="角色">
          <el-tag :type="formData.role === 'admin' ? 'danger' : 'primary'" size="large">
            {{ formData.role === 'admin' ? '管理员' : '用户' }}
          </el-tag>
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input 
            v-model="formData.email" 
            placeholder="请输入邮箱"
            size="large"
            :prefix-icon="Message"
          />
        </el-form-item>
        
        <el-form-item label="手机号" prop="phone">
          <el-input 
            v-model="formData.phone" 
            placeholder="请输入手机号"
            size="large"
            :prefix-icon="Phone"
          />
        </el-form-item>
        
        <el-form-item label="真实姓名" prop="realName">
          <el-input 
            v-model="formData.realName" 
            placeholder="请输入真实姓名"
            size="large"
            :prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item label="新密码" prop="password">
          <el-input 
            v-model="formData.password" 
            type="password" 
            placeholder="留空则不修改密码"
            show-password
            size="large"
            :prefix-icon="Lock"
          />
          <span class="form-tip">留空则不修改密码</span>
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input 
            v-model="formData.confirmPassword" 
            type="password" 
            placeholder="请再次输入新密码"
            show-password
            size="large"
            :prefix-icon="Lock"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            @click="handleSave" 
            :loading="saving"
            size="large"
          >
            保存修改
          </el-button>
          <el-button 
            @click="handleReset" 
            size="large"
          >
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Lock, Message, Phone } from '@element-plus/icons-vue'
import request from '../utils/request'

export default {
  name: 'UserProfile',
  components: {
    User,
    Lock,
    Message,
    Phone
  },
  setup() {
    const formData = ref({})
    const formRef = ref(null)
    const saving = ref(false)
    const originalData = ref({})

    const validateConfirmPassword = (rule, value, callback) => {
      if (formData.value.password && value !== formData.value.password) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }

    const formRules = {
      email: [
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      phone: [
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
      ],
      confirmPassword: [
        { validator: validateConfirmPassword, trigger: 'blur' }
      ]
    }

    const loadUserInfo = async () => {
      try {
        const userInfoStr = localStorage.getItem('userInfo')
        if (!userInfoStr) {
          ElMessage.error('未找到用户信息')
          return
        }

        const userInfo = JSON.parse(userInfoStr)
        const response = await request.get('/user/profile', {
          params: { username: userInfo.username }
        })

        if (response.code === 200 && response.data) {
          formData.value = {
            id: response.data.id,
            username: response.data.username,
            email: response.data.email || '',
            phone: response.data.phone || '',
            realName: response.data.realName || '',
            role: response.data.role,
            password: '',
            confirmPassword: ''
          }
          originalData.value = { ...formData.value }
        } else {
          ElMessage.error(response.message || '加载用户信息失败')
        }
      } catch (error) {
        console.error('加载用户信息失败:', error)
        ElMessage.error('加载用户信息失败: ' + (error.message || '未知错误'))
      }
    }

    const handleSave = async () => {
      if (!formRef.value) return

      await formRef.value.validate(async (valid) => {
        if (valid) {
          saving.value = true
          try {
            const userInfoStr = localStorage.getItem('userInfo')
            if (!userInfoStr) {
              ElMessage.error('未找到用户信息')
              return
            }

            const userInfo = JSON.parse(userInfoStr)
            const updateData = {
              username: userInfo.username,
              email: formData.value.email,
              phone: formData.value.phone,
              realName: formData.value.realName
            }

            // 如果输入了新密码，则更新
            if (formData.value.password && formData.value.password.trim() !== '') {
              updateData.password = formData.value.password
            }

            const response = await request.put('/user/profile', updateData)
            if (response.code === 200) {
              ElMessage.success('修改成功')
              
              // 更新本地存储的用户信息
              const updatedUserInfo = {
                ...userInfo,
                email: formData.value.email,
                phone: formData.value.phone,
                realName: formData.value.realName
              }
              localStorage.setItem('userInfo', JSON.stringify(updatedUserInfo))
              
              // 清空密码字段
              formData.value.password = ''
              formData.value.confirmPassword = ''
              originalData.value = { ...formData.value }
            } else {
              ElMessage.error(response.message || '修改失败')
            }
          } catch (error) {
            ElMessage.error('修改失败: ' + (error.message || '未知错误'))
          } finally {
            saving.value = false
          }
        }
      })
    }

    const handleReset = () => {
      ElMessageBox.confirm('确定要重置所有修改吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        formData.value = { ...originalData.value }
        formData.value.password = ''
        formData.value.confirmPassword = ''
        if (formRef.value) {
          formRef.value.clearValidate()
        }
        ElMessage.success('已重置')
      }).catch(() => {})
    }

    onMounted(() => {
      loadUserInfo()
    })

    return {
      formData,
      formRef,
      saving,
      formRules,
      handleSave,
      handleReset,
      User,
      Lock,
      Message,
      Phone
    }
  }
}
</script>

<style scoped>
.user-profile {
  padding: 0;
}

.main-card {
  background-color: #faf9f5;
  border: 1px solid #e6dfd8;
  border-radius: 12px;
}

.main-card :deep(.el-card__header) {
  background-color: #faf9f5;
  border-bottom: 1px solid #ebe6df;
  padding: 24px 32px;
}

.card-header h3 {
  margin: 0 0 6px 0;
  color: #141413;
  font-family: 'Cormorant Garamond', 'EB Garamond', 'Times New Roman', serif;
  font-size: 28px;
  font-weight: 400;
  letter-spacing: -0.3px;
}

.subtitle {
  margin: 0;
  color: #6c6a64;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
}

.profile-form {
  max-width: 600px;
  margin: 32px auto;
}

.form-tip {
  margin-left: 10px;
  color: #8e8b82;
  font-size: 12px;
  font-family: 'Inter', sans-serif;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #3d3d3a;
}

:deep(.el-input.is-disabled .el-input__wrapper) {
  background-color: #f5f0e8;
}
</style>




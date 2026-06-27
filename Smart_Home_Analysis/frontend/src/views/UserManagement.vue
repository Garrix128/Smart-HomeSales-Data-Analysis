<template>
  <div class="user-management">
    <el-card shadow="never" class="main-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <h3>用户管理</h3>
            <p class="subtitle">管理系统用户，支持新增、编辑、删除和启用/禁用操作</p>
          </div>
          <el-button type="primary" @click="handleAdd" :icon="Plus">新增用户</el-button>
        </div>
      </template>
      
      <div class="toolbar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索用户名、邮箱、真实姓名"
          style="width: 350px; margin-right: 10px"
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button @click="loadData" :icon="Refresh">刷新</el-button>
      </div>
      
      <el-table
        :data="tableData"
        style="width: 100%"
        border
        v-loading="loading"
        stripe
        :height="600"
        class="data-table"
      >
        <el-table-column prop="id" label="ID" width="80" fixed="left" />
        <el-table-column prop="username" label="用户名" width="150" show-overflow-tooltip />
        <el-table-column prop="email" label="邮箱" width="200" show-overflow-tooltip />
        <el-table-column prop="realName" label="真实姓名" width="120" />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.role === 'admin' ? 'danger' : 'primary'">
              {{ scope.row.role === 'admin' ? '管理员' : '用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
              {{ scope.row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDateTime(scope.row.createTime) }}
          </template>
        </el-table-column>
        <el-table-column prop="lastLoginTime" label="最后登录" width="180">
          <template #default="scope">
            {{ scope.row.lastLoginTime ? formatDateTime(scope.row.lastLoginTime) : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" @click="handleEdit(scope.row)" :icon="Edit">编辑</el-button>
            <el-button 
              size="small" 
              :type="scope.row.status === 1 ? 'warning' : 'success'"
              @click="handleToggleStatus(scope.row)"
            >
              {{ scope.row.status === 1 ? '禁用' : '启用' }}
            </el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row.id)" :icon="Delete">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          :current-page="currentPage"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <el-form
        :model="formData"
        label-width="100px"
        :rules="formRules"
        ref="formRef"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="formData.username" />
        </el-form-item>
        <el-form-item label="密码" :prop="formData.id ? '' : 'password'">
          <el-input v-model="formData.password" type="password" show-password :placeholder="formData.id ? '留空则不修改密码' : '请输入密码'" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formData.email" />
        </el-form-item>
        <el-form-item label="真实姓名" prop="realName">
          <el-input v-model="formData.realName" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="formData.role" placeholder="请选择角色" style="width: 100%">
            <el-option label="管理员" value="admin" />
            <el-option label="用户" value="user" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="formData.status" placeholder="请选择状态" style="width: 100%">
            <el-option label="启用" :value="1" />
            <el-option label="禁用" :value="0" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, Refresh, Edit, Delete } from '@element-plus/icons-vue'
import request from '../utils/request'

export default {
  name: 'UserManagement',
  components: {
    Search,
    Plus,
    Refresh,
    Edit,
    Delete
  },
  setup() {
    const tableData = ref([])
    const loading = ref(false)
    const dialogVisible = ref(false)
    const dialogTitle = ref('新增用户')
    const formData = ref({})
    const formRef = ref(null)
    const saving = ref(false)
    const searchKeyword = ref('')
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)

    const formRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
      ],
      role: [
        { required: true, message: '请选择角色', trigger: 'change' }
      ],
      status: [
        { required: true, message: '请选择状态', trigger: 'change' }
      ]
    }

    const loadData = async () => {
      loading.value = true
      try {
        const params = {
          page: currentPage.value || 1,
          size: pageSize.value || 10,
          search: searchKeyword.value || ''
        }
        
        const response = await request.get('/user/manage/page', {
          params: params,
          timeout: 15000
        })
        
        if (response.code === 200 && response.data) {
          tableData.value = response.data.records || []
          total.value = response.data.total || 0
        } else {
          ElMessage.error(response.message || '加载数据失败')
          tableData.value = []
          total.value = 0
        }
      } catch (error) {
        console.error('加载数据错误:', error)
        ElMessage.error('加载数据失败: ' + (error.message || '网络错误'))
        tableData.value = []
        total.value = 0
      } finally {
        loading.value = false
      }
    }

    const handleSearch = () => {
      currentPage.value = 1
      loadData()
    }

    const handleAdd = () => {
      formData.value = {
        username: '',
        password: '',
        email: '',
        realName: '',
        role: 'user',
        status: 1
      }
      dialogTitle.value = '新增用户'
      dialogVisible.value = true
    }

    const handleEdit = (row) => {
      formData.value = {
        id: row.id,
        username: row.username,
        password: '',
        email: row.email || '',
        realName: row.realName || '',
        role: row.role,
        status: row.status
      }
      dialogTitle.value = '编辑用户'
      dialogVisible.value = true
    }

    const handleDelete = async (id) => {
      ElMessageBox.confirm('确定删除该用户吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await request.delete(`/user/manage/${id}`)
          ElMessage.success('删除成功')
          loadData()
        } catch (error) {
          ElMessage.error('删除失败: ' + (error.message || '未知错误'))
        }
      }).catch(() => {})
    }

    const handleToggleStatus = async (row) => {
      const newStatus = row.status === 1 ? 0 : 1
      const action = newStatus === 1 ? '启用' : '禁用'
      
      ElMessageBox.confirm(`确定${action}该用户吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await request.put(`/user/manage/${row.id}/status`, { status: newStatus })
          ElMessage.success(`${action}成功`)
          loadData()
        } catch (error) {
          ElMessage.error(`${action}失败: ` + (error.message || '未知错误'))
        }
      }).catch(() => {})
    }

    const handleSave = async () => {
      if (!formRef.value) return
      
      await formRef.value.validate(async (valid) => {
        if (valid) {
          saving.value = true
          try {
            const data = { ...formData.value }
            // 如果是编辑且密码为空，则不传密码字段
            if (data.id && (!data.password || data.password.trim() === '')) {
              delete data.password
            }
            
            if (data.id) {
              await request.put('/user/manage', data)
              ElMessage.success('更新成功')
            } else {
              await request.post('/user/manage', data)
              ElMessage.success('新增成功')
            }
            dialogVisible.value = false
            loadData()
          } catch (error) {
            ElMessage.error('保存失败: ' + (error.message || '未知错误'))
          } finally {
            saving.value = false
          }
        }
      })
    }

    const handleSizeChange = (val) => {
      pageSize.value = val
      currentPage.value = 1
      loadData()
    }

    const handleCurrentChange = (val) => {
      currentPage.value = val
      loadData()
    }

    const formatDateTime = (dateTimeStr) => {
      if (!dateTimeStr) return '-'
      try {
        const date = new Date(dateTimeStr)
        const year = date.getFullYear()
        const month = String(date.getMonth() + 1).padStart(2, '0')
        const day = String(date.getDate()).padStart(2, '0')
        const hours = String(date.getHours()).padStart(2, '0')
        const minutes = String(date.getMinutes()).padStart(2, '0')
        const seconds = String(date.getSeconds()).padStart(2, '0')
        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
      } catch (error) {
        return dateTimeStr
      }
    }

    onMounted(() => {
      loadData()
    })

    return {
      tableData,
      loading,
      dialogVisible,
      dialogTitle,
      formData,
      formRef,
      saving,
      searchKeyword,
      currentPage,
      pageSize,
      total,
      formRules,
      loadData,
      handleSearch,
      handleAdd,
      handleEdit,
      handleDelete,
      handleToggleStatus,
      handleSave,
      handleSizeChange,
      handleCurrentChange,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.user-management {
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left h3 {
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
  font-size: 14px;
  font-family: 'Inter', sans-serif;
}

.toolbar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.data-table {
  margin-bottom: 20px;
}

.pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>


<template>
  <div class="data-management">
    <el-card shadow="never" class="main-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <h3>数据管理</h3>
            <p class="subtitle">清洗合并数据的管理，支持查询、新增、编辑和删除操作</p>
          </div>
          <el-button type="primary" @click="handleAdd" :icon="Plus">新增数据</el-button>
        </div>
      </template>
      
      <div class="toolbar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索订单编号、产品型号、品牌、省份等"
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
        <el-table-column prop="订单编号" label="订单编号" width="150" show-overflow-tooltip />
        <el-table-column prop="产品型号" label="产品型号" width="150" show-overflow-tooltip />
        <el-table-column prop="销售渠道" label="销售渠道" width="120" />
        <el-table-column prop="用户所在省份" label="省份" width="120" />
        <el-table-column prop="用户性别" label="性别" width="80" />
        <el-table-column prop="是否会员" label="是否会员" width="100" />
        <el-table-column prop="会员等级" label="会员等级" width="100" />
        <el-table-column prop="促销类型" label="促销类型" width="120" />
        <el-table-column prop="促销折扣率" label="折扣率" width="100" />
        <el-table-column prop="订单日期" label="订单日期" width="120" />
        <el-table-column prop="是否节假日" label="是否节假日" width="100" />
        <el-table-column prop="产品品类" label="产品品类" width="120" />
        <el-table-column prop="品牌名称" label="品牌" width="120" />
        <el-table-column prop="销售单价" label="单价" width="100" />
        <el-table-column prop="销售数量" label="数量" width="80" />
        <el-table-column prop="订单总金额" label="总金额" width="120" />
        <el-table-column prop="处理时间" label="处理时间" width="150" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" @click="handleEdit(scope.row)" :icon="Edit">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row.id)" :icon="Delete">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100, 200]"
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
      width="700px"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <el-form
        :model="formData"
        label-width="120px"
        :rules="formRules"
        ref="formRef"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="订单编号" prop="订单编号">
              <el-input v-model="formData.订单编号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="产品型号" prop="产品型号">
              <el-input v-model="formData.产品型号" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="销售渠道">
              <el-input v-model="formData.销售渠道" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="用户所在省份">
              <el-input v-model="formData.用户所在省份" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用户性别">
              <el-select v-model="formData.用户性别" placeholder="请选择" style="width: 100%">
                <el-option label="男" value="男" />
                <el-option label="女" value="女" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="是否会员">
              <el-select v-model="formData.是否会员" placeholder="请选择" style="width: 100%">
                <el-option label="是" value="是" />
                <el-option label="否" value="否" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="会员等级">
              <el-input v-model="formData.会员等级" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="促销类型">
              <el-input v-model="formData.促销类型" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="促销折扣率">
              <el-input v-model="formData.促销折扣率" type="number" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="订单日期">
              <el-input v-model="formData.订单日期" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="是否节假日">
              <el-select v-model="formData.是否节假日" placeholder="请选择" style="width: 100%">
                <el-option label="是" value="是" />
                <el-option label="否" value="否" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="产品品类">
              <el-input v-model="formData.产品品类" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="品牌名称">
              <el-input v-model="formData.品牌名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="销售单价">
              <el-input v-model="formData.销售单价" type="number" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="销售数量">
              <el-input v-model="formData.销售数量" type="number" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="订单总金额">
              <el-input v-model="formData.订单总金额" type="number" />
            </el-form-item>
          </el-col>
        </el-row>
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
  name: 'DataManagement',
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
    const dialogTitle = ref('新增数据')
    const formData = ref({})
    const formRef = ref(null)
    const saving = ref(false)
    const searchKeyword = ref('')
    const currentPage = ref(1)
    const pageSize = ref(10) // 减少默认页面大小，提升加载速度
    const total = ref(0)
    const allData = ref([])

    const formRules = {
      订单编号: [
        { required: true, message: '请输入订单编号', trigger: 'blur' }
      ],
      产品型号: [
        { required: true, message: '请输入产品型号', trigger: 'blur' }
      ]
    }

    const loadData = async () => {
      loading.value = true
      try {
        // 确保分页参数正确传递
        const params = {
          page: currentPage.value || 1,
          size: pageSize.value || 10,
          search: searchKeyword.value || ''
        }
        
        const response = await request.get('/data/manage/merged-data/page', {
          params: params,
          timeout: 15000 // 15秒超时
        })
        if (response.code === 200 && response.data) {
          // MyBatis Plus Page对象包含records和total字段
          tableData.value = response.data.records || []
          total.value = response.data.total || 0
          
          // 如果没有数据，给出提示
          if (tableData.value.length === 0 && currentPage.value === 1) {
            ElMessage.info('暂无数据')
          }
        } else {
          ElMessage.error(response.message || '加载数据失败')
          tableData.value = []
          total.value = 0
        }
      } catch (error) {
        console.error('加载数据错误:', error)
        let errorMsg = '加载数据失败'
        if (error.code === 'ECONNABORTED') {
          errorMsg = '请求超时，请检查网络连接或减少查询条件'
        } else if (error.response) {
          errorMsg = error.response.data?.message || error.message || '服务器错误'
        } else if (error.message) {
          errorMsg = error.message
        }
        ElMessage.error(errorMsg)
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
        订单编号: '',
        产品型号: '',
        销售渠道: '',
        用户所在省份: '',
        用户性别: '',
        是否会员: '',
        会员等级: '',
        促销类型: '',
        促销折扣率: '',
        订单日期: '',
        是否节假日: '',
        产品品类: '',
        品牌名称: '',
        销售单价: '',
        销售数量: '',
        订单总金额: ''
      }
      dialogTitle.value = '新增数据'
      dialogVisible.value = true
    }

    const handleEdit = (row) => {
      formData.value = { ...row }
      dialogTitle.value = '编辑数据'
      dialogVisible.value = true
    }

    const handleDelete = async (id) => {
      ElMessageBox.confirm('确定删除这条数据吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await request.delete(`/data/manage/merged-data/${id}`)
          ElMessage.success('删除成功')
          loadData()
        } catch (error) {
          ElMessage.error('删除失败: ' + (error.message || '未知错误'))
        }
      }).catch(() => {})
    }

    const handleSave = async () => {
      if (!formRef.value) return
      
      await formRef.value.validate(async (valid) => {
        if (valid) {
          saving.value = true
          try {
            if (formData.value.id) {
              await request.put('/data/manage/merged-data', formData.value)
              ElMessage.success('更新成功')
            } else {
              await request.post('/data/manage/merged-data', formData.value)
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
      currentPage.value = 1 // 改变页面大小时重置到第一页
      loadData()
    }

    const handleCurrentChange = (val) => {
      currentPage.value = val
      loadData()
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
      handleSave,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.data-management {
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

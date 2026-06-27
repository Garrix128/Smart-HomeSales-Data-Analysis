<template>
  <el-container class="layout-container">
    <el-aside width="200px" class="sidebar">
      <div class="logo">
        <h2 class="logo-text">Smart Home</h2>
        <span class="logo-subtitle">数据分析系统</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="sidebar-menu"
        router
        background-color="#181715"
        text-color="#a09d96"
        active-text-color="#cc785c"
      >
        <!-- 管理员菜单 -->
        <template v-if="isAdmin">
          <el-menu-item index="/data-management">
            <el-icon><Document /></el-icon>
            <span>数据管理</span>
          </el-menu-item>
          <el-menu-item index="/user-management">
            <el-icon><UserFilled /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
        </template>
        <!-- 可视化分析（管理员和用户都有） -->
        <el-sub-menu index="/visualization">
          <template #title>
            <el-icon><DataAnalysis /></el-icon>
            <span>可视化分析</span>
          </template>
          <el-menu-item index="/visualization/sales-trend">
            <span>销售趋势分析</span>
          </el-menu-item>
          <el-menu-item index="/visualization/region">
            <span>地域分析</span>
          </el-menu-item>
          <el-menu-item index="/visualization/product">
            <span>产品分析</span>
          </el-menu-item>
          <el-menu-item index="/visualization/user-profile">
            <span>用户画像分析</span>
          </el-menu-item>
          <el-menu-item index="/visualization/promotion">
            <span>促销效果分析</span>
          </el-menu-item>
          <el-menu-item index="/visualization/prediction">
            <span>随机森林预测</span>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <div class="header-actions">
            <el-dropdown @command="handleCommand">
              <span class="user-info">
                <el-icon><User /></el-icon>
                {{ userInfo?.username || '用户' }}
                <el-icon class="el-icon--right"><arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                  <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Document, DataAnalysis, User, ArrowDown, UserFilled } from '@element-plus/icons-vue'

export default {
  name: 'Layout',
  components: {
    Document,
    DataAnalysis,
    User,
    ArrowDown,
    UserFilled
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const userInfo = ref(null)
    
    const activeMenu = computed(() => {
      return route.path
    })
    
    const isAdmin = computed(() => {
      return userInfo.value && userInfo.value.role === 'admin'
    })
    
    const pageTitle = computed(() => {
      const titles = {
        '/data-management': '数据管理',
        '/user-management': '用户管理',
        '/visualization': '可视化分析',
        '/visualization/sales-trend': '销售趋势分析（时间维度）',
        '/visualization/region': '地域分析（地区维度）',
        '/visualization/product': '产品分析（产品维度）',
        '/visualization/user-profile': '用户画像分析（用户维度）',
        '/visualization/promotion': '促销效果分析（促销维度）',
        '/visualization/prediction': '随机森林预测模型',
        '/user-profile': '个人信息'
      }
      return titles[route.path] || '数据分析系统'
    })
    
    const handleCommand = (command) => {
      if (command === 'logout') {
        localStorage.removeItem('token')
        localStorage.removeItem('userInfo')
        ElMessage.success('已退出登录')
        router.push('/login')
      } else if (command === 'profile') {
        router.push('/user-profile')
      }
    }
    
    onMounted(() => {
      const userInfoStr = localStorage.getItem('userInfo')
      if (userInfoStr) {
        userInfo.value = JSON.parse(userInfoStr)
      }
    })
    
    return {
      activeMenu,
      pageTitle,
      userInfo,
      isAdmin,
      handleCommand
    }
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.sidebar {
  background-color: #181715;
  overflow: hidden;
}

.logo {
  height: 64px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #181715;
  border-bottom: 1px solid rgba(250, 249, 245, 0.08);
  padding: 0 16px;
}

.logo-text {
  font-family: 'Cormorant Garamond', 'EB Garamond', 'Times New Roman', serif;
  font-size: 20px;
  font-weight: 400;
  color: #faf9f5;
  letter-spacing: -0.3px;
  margin: 0;
  line-height: 1.2;
}

.logo-subtitle {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  font-weight: 400;
  color: #a09d96;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.sidebar-menu {
  border: none;
  height: calc(100vh - 64px);
  overflow-y: auto;
}

.sidebar-menu :deep(.el-sub-menu__title) {
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 500;
}

.sidebar-menu :deep(.el-menu-item) {
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 400;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background-color: rgba(204, 120, 92, 0.12);
  border-right: 2px solid #cc785c;
}

.header {
  background-color: #faf9f5;
  border-bottom: 1px solid #e6dfd8;
  padding: 0 24px;
  height: 64px;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  height: 100%;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #3d3d3a;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: 8px;
  transition: background-color 0.15s ease;
}

.user-info:hover {
  background-color: #efe9de;
}

.main-content {
  background-color: #faf9f5;
  padding: 24px;
  overflow-y: auto;
  min-height: calc(100vh - 64px);
}
</style>


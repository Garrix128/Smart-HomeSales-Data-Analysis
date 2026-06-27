import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
import Layout from '../components/Layout.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: Layout,
    meta: { requiresAuth: true },
    redirect: '/visualization/sales-trend',
    children: [
      {
        path: 'data-management',
        name: 'DataManagement',
        component: () => import('../views/DataManagement.vue'),
        meta: { requiresAdmin: true }
      },
      {
        path: 'user-management',
        name: 'UserManagement',
        component: () => import('../views/UserManagement.vue'),
        meta: { requiresAdmin: true }
      },
      {
        path: 'visualization/sales-trend',
        name: 'SalesTrend',
        component: () => import('../views/visualization/SalesTrend.vue')
      },
      {
        path: 'visualization/region',
        name: 'RegionAnalysis',
        component: () => import('../views/visualization/RegionAnalysis.vue')
      },
      {
        path: 'visualization/product',
        name: 'ProductAnalysis',
        component: () => import('../views/visualization/ProductAnalysis.vue')
      },
      {
        path: 'visualization/user-profile',
        name: 'UserProfileAnalysis',
        component: () => import('../views/visualization/UserProfileAnalysis.vue')
      },
      {
        path: 'visualization/promotion',
        name: 'PromotionAnalysis',
        component: () => import('../views/visualization/PromotionAnalysis.vue')
      },
      {
        path: 'visualization/prediction',
        name: 'Prediction',
        component: () => import('../views/visualization/Prediction.vue')
      },
      {
        path: 'user-profile',
        name: 'UserProfile',
        component: () => import('../views/UserProfile.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userInfoStr = localStorage.getItem('userInfo')
  let userInfo = null
  
  if (userInfoStr) {
    try {
      userInfo = JSON.parse(userInfoStr)
    } catch (e) {
      localStorage.removeItem('userInfo')
      localStorage.removeItem('token')
    }
  }
  
  // 如果访问的不是登录页和注册页，且没有token和userInfo，强制跳转到登录页
  if (to.path !== '/login' && to.path !== '/register') {
    if (!token || !userInfo) {
      // 清除可能存在的无效token
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      next('/login')
      return
    }
    
    // 检查是否需要管理员权限
    if (to.meta.requiresAdmin && userInfo.role !== 'admin') {
      ElMessage.error('您没有权限访问此页面')
      next('/visualization/sales-trend')
      return
    }
    
    // 如果访问根路径，根据角色跳转
    if (to.path === '/') {
      if (userInfo.role === 'admin') {
        next('/data-management')
        return
      } else {
        next('/visualization/sales-trend')
        return
      }
    }
  }
  
  // 如果访问登录页或注册页，但已经登录，根据角色跳转
  if (to.path === '/login' || to.path === '/register') {
    if (token && userInfo) {
      if (userInfo.role === 'admin') {
        next('/data-management')
      } else {
        next('/visualization/sales-trend')
      }
      return
    }
  }
  
  // 其他情况正常跳转
  next()
})

export default router


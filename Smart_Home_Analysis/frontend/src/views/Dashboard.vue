<template>
  <div class="dashboard">
    <el-container>
      <el-main>
        <el-row :gutter="20">
          <!-- 销售趋势图 -->
          <el-col :span="24">
            <el-card class="chart-card">
              <template #header>
                <div class="card-title">销售额时间趋势图</div>
              </template>
              <SalesTrendChart />
            </el-card>
          </el-col>
        </el-row>
        
        <el-row :gutter="20" style="margin-top: 20px">
          <!-- 地域分布图 -->
          <el-col :span="12">
            <el-card class="chart-card">
              <template #header>
                <div class="card-title">地域分布热力图</div>
              </template>
              <RegionMap />
            </el-card>
          </el-col>
          
          <!-- 产品品类占比图 -->
          <el-col :span="12">
            <el-card class="chart-card">
              <template #header>
                <div class="card-title">产品品类占比图</div>
              </template>
              <ProductAnalysis />
            </el-card>
          </el-col>
        </el-row>
        
        <el-row :gutter="20" style="margin-top: 20px">
          <!-- 销售渠道分析图 -->
          <el-col :span="12">
            <el-card class="chart-card">
              <template #header>
                <div class="card-title">销售渠道分析图</div>
              </template>
              <ChannelAnalysis />
            </el-card>
          </el-col>
          
          <!-- 用户画像分析图 -->
          <el-col :span="12">
            <el-card class="chart-card">
              <template #header>
                <div class="card-title">用户画像分析图</div>
              </template>
              <UserProfileChart />
            </el-card>
          </el-col>
        </el-row>
        
        <el-row :gutter="20" style="margin-top: 20px">
          <!-- 随机森林特征重要性图 -->
          <el-col :span="24">
            <el-card class="chart-card">
              <template #header>
                <div class="card-title">随机森林特征重要性图</div>
              </template>
              <RandomForestChart />
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import SalesTrendChart from '../components/SalesTrendChart.vue'
import RegionMap from '../components/RegionMap.vue'
import ProductAnalysis from '../components/ProductAnalysis.vue'
import ChannelAnalysis from '../components/ChannelAnalysis.vue'
import UserProfileChart from '../components/UserProfileChart.vue'
import RandomForestChart from '../components/RandomForestChart.vue'

export default {
  name: 'Dashboard',
  components: {
    SalesTrendChart,
    RegionMap,
    ProductAnalysis,
    ChannelAnalysis,
    UserProfileChart,
    RandomForestChart
  },
  setup() {
    const router = useRouter()
    
    return {}
  }
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.header-content h1 {
  margin: 0;
  color: #303133;
  font-size: 24px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.chart-card {
  height: 100%;
  min-height: 400px;
}

.el-main {
  padding: 20px;
}
</style>


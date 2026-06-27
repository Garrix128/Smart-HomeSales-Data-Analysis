<template>
  <div class="visualization-page">
    <el-card shadow="never" class="chart-card">
      <template #header>
        <div class="card-header">
          <div class="header-content">
            <h3>地域分析（地区维度）</h3>
            <p class="subtitle">展示不同地区的销售分布情况，包括各地区总销售额、订单数和用户数</p>
          </div>
        </div>
      </template>
      <RegionMap />
    </el-card>
  </div>
</template>

<script>
import RegionMap from '../../components/RegionMap.vue'

export default {
  name: 'RegionAnalysis',
  components: {
    RegionMap
  }
}
</script>

<style scoped>
.visualization-page {
  padding: 0;
}

.chart-card {
  background-color: #faf9f5;
  border: 1px solid #e6dfd8;
  border-radius: 12px;
}

.chart-card :deep(.el-card__header) {
  background-color: #faf9f5;
  border-bottom: 1px solid #ebe6df;
  padding: 24px 32px;
}

.chart-card :deep(.el-card__body) {
  padding: 24px 32px;
}

.card-header h3 {
  margin: 0 0 8px 0;
  color: #141413;
  font-family: 'Cormorant Garamond', 'EB Garamond', 'Times New Roman', serif;
  font-size: 28px;
  font-weight: 400;
  line-height: 1.2;
  letter-spacing: -0.3px;
}

.subtitle {
  margin: 0;
  color: #6c6a64;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.55;
}
</style>

<template>
  <div class="visualization-page">
    <el-card shadow="never" class="chart-card">
      <template #header>
        <div class="card-header">
          <div class="header-content">
            <h3>销售趋势分析（时间维度）</h3>
            <p class="subtitle">展示销售额随时间的变化趋势，包括每日销售额、订单数和平均订单金额</p>
          </div>
        </div>
      </template>
      <SalesTrendChart />
    </el-card>
  </div>
</template>

<script>
import SalesTrendChart from '../../components/SalesTrendChart.vue'

export default {
  name: 'SalesTrend',
  components: {
    SalesTrendChart
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

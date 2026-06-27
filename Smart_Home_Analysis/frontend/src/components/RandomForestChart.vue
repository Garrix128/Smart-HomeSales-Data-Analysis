<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="never" class="chart-card">
          <template #header>
            <div class="card-title">预测结果对比</div>
          </template>
          <div ref="predictionChartRef" style="width: 100%; height: 450px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="never" class="chart-card">
          <template #header>
            <div class="card-title">特征重要性</div>
          </template>
          <div ref="featureChartRef" style="width: 100%; height: 450px;"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card shadow="never" class="chart-card">
          <template #header>
            <div class="card-title">模型评估指标</div>
          </template>
          <el-descriptions :column="3" border>
            <el-descriptions-item label="RMSE (均方根误差)">
              <el-tag :type="getMetricType(metrics.rmse, 'rmse')">
                {{ metrics.rmse ? metrics.rmse.toFixed(2) : '--' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="MAE (平均绝对误差)">
              <el-tag :type="getMetricType(metrics.mae, 'mae')">
                {{ metrics.mae ? metrics.mae.toFixed(2) : '--' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="R² (决定系数)">
              <el-tag :type="getMetricType(metrics.r2, 'r2')">
                {{ metrics.r2 ? metrics.r2.toFixed(4) : '--' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="平均相对误差">
              <el-tag :type="getMetricType(metrics.avgRelativeError, 'error')">
                {{ metrics.avgRelativeError ? metrics.avgRelativeError.toFixed(2) + '%' : '--' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="预测样本数">
              <el-tag type="info">{{ metrics.sampleCount || 0 }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="预测目标">
              <el-tag type="info">{{ metrics.targetType || '--' }}</el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import request from '../utils/request'

export default {
  name: 'RandomForestChart',
  setup() {
    const predictionChartRef = ref(null)
    const featureChartRef = ref(null)
    let predictionChartInstance = null
    let featureChartInstance = null
    const metrics = ref({
      rmse: null,
      mae: null,
      r2: null,
      avgRelativeError: null,
      sampleCount: 0,
      targetType: null
    })

    const getMetricType = (value, type) => {
      if (value === null || value === undefined) return 'info'
      if (type === 'r2') {
        if (value >= 0.8) return 'success'
        if (value >= 0.6) return 'warning'
        return 'danger'
      }
      if (type === 'error') {
        if (value <= 10) return 'success'
        if (value <= 20) return 'warning'
        return 'danger'
      }
      return 'info'
    }

    const initPredictionChart = (predictions) => {
      if (!predictionChartRef.value) return
      
      predictionChartInstance = echarts.init(predictionChartRef.value)
      
      const sampleSize = Math.min(50, predictions.length)
      const sampleData = predictions.slice(0, sampleSize)
      
      const predicted = sampleData.map(item => parseFloat(item.predictedSales || item.predicted_sales || 0))
      const actual = sampleData.map(item => parseFloat(item.actualSales || item.actual_sales || 0))
      const indices = sampleData.map((_, index) => index + 1)
      
      const option = {
        backgroundColor: 'transparent',
        title: {
          text: '预测值 vs 实际值对比',
          left: 'center',
          top: 0,
          textStyle: { fontSize: 16, fontWeight: 500, color: '#141413', fontFamily: 'Inter, sans-serif' }
        },
        tooltip: {
          trigger: 'axis',
          backgroundColor: '#181715',
          borderColor: '#252320',
          padding: [10, 14],
          textStyle: { color: '#faf9f5', fontSize: 13, fontFamily: 'Inter, sans-serif' },
          formatter: function(params) {
            let result = `<div style="font-weight:500;margin-bottom:8px;color:#a09d96;font-size:11px;letter-spacing:1px;">样本 ${params[0].axisValue}</div>`
            params.forEach(param => {
              result += `<div style="margin:4px 0;font-size:13px;">${param.marker}${param.seriesName}: <span style="font-weight:500;">${param.value.toLocaleString()}</span></div>`
            })
            return result
          }
        },
        legend: {
          data: ['预测值', '实际值'],
          top: 30,
          textStyle: { fontSize: 13, color: '#6c6a64', fontFamily: 'Inter, sans-serif' },
          itemGap: 30
        },
        grid: { left: '3%', right: '4%', bottom: '3%', top: '20%', containLabel: true },
        xAxis: {
          type: 'category',
          data: indices,
          name: '样本序号',
          axisLabel: { rotate: 0, fontSize: 12, color: '#6c6a64', fontFamily: 'Inter, sans-serif' },
          axisLine: { lineStyle: { color: '#e6dfd8', width: 1 } },
          axisTick: { show: false }
        },
        yAxis: {
          type: 'value',
          name: '数值',
          axisLabel: {
            formatter: function(v) { return v >= 10000 ? (v / 10000).toFixed(1) + '万' : v.toLocaleString(); },
            fontSize: 12, color: '#6c6a64', fontFamily: 'Inter, sans-serif'
          },
          axisLine: { show: true, lineStyle: { color: '#cc785c', width: 2 } },
          splitLine: { lineStyle: { color: '#e6dfd8', type: 'dashed', width: 1 } }
        },
        series: [
          {
            name: '预测值',
            type: 'line',
            data: predicted,
            itemStyle: { color: '#cc785c' },
            lineStyle: { width: 3, shadowBlur: 5, shadowColor: 'rgba(204,120,92,0.25)' },
            symbol: 'circle',
            symbolSize: 7,
            areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: 'rgba(204,120,92,0.2)' }, { offset: 1, color: 'rgba(204,120,92,0.02)' }]) },
            emphasis: { focus: 'series', itemStyle: { borderColor: '#faf9f5', borderWidth: 2, shadowBlur: 10, shadowColor: 'rgba(204,120,92,0.4)' } }
          },
          {
            name: '实际值',
            type: 'line',
            data: actual,
            itemStyle: { color: '#e8a55a' },
            lineStyle: { width: 3, shadowBlur: 5, shadowColor: 'rgba(232,165,90,0.3)', type: 'dashed' },
            symbol: 'circle',
            symbolSize: 7,
            emphasis: { focus: 'series', itemStyle: { borderColor: '#faf9f5', borderWidth: 2, shadowBlur: 10, shadowColor: 'rgba(232,165,90,0.4)' } }
          }
        ]
      }
      
      predictionChartInstance.setOption(option)
    }

    const initFeatureChart = (features) => {
      if (!featureChartRef.value) return
      
      featureChartInstance = echarts.init(featureChartRef.value)
      
      // 去掉特征名称中的 "_indexed" 后缀
      const featureNames = features.map(item => {
        const name = item.featureName || item.feature_name || '未知'
        return name.replace(/_indexed$/, '')
      })
      const importances = features.map(item => parseFloat(item.importance || 0))
      
      const option = {
        backgroundColor: 'transparent',
        title: {
          text: '特征重要性排名',
          left: 'center',
          top: 0,
          textStyle: { fontSize: 16, fontWeight: 500, color: '#141413', fontFamily: 'Inter, sans-serif' }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' },
          backgroundColor: '#181715',
          borderColor: '#252320',
          padding: [10, 14],
          textStyle: { color: '#faf9f5', fontSize: 13, fontFamily: 'Inter, sans-serif' },
          formatter: function(params) {
            return `<div style="font-weight:500;margin-bottom:8px;font-size:13px;">${params[0].name}</div><div style="font-size:13px;">重要性: <span style="font-weight:500;color:#cc785c;">${params[0].value.toFixed(6)}</span></div>`
          }
        },
        grid: { left: '3%', right: '4%', bottom: '3%', top: '12%', containLabel: true },
        xAxis: {
          type: 'value',
          name: '重要性',
          axisLabel: { fontSize: 12, color: '#6c6a64', fontFamily: 'Inter, sans-serif' },
          axisLine: { show: true, lineStyle: { color: '#cc785c', width: 2 } },
          splitLine: { lineStyle: { color: '#e6dfd8', type: 'dashed', width: 1 } }
        },
        yAxis: {
          type: 'category',
          data: featureNames,
          inverse: true,
          axisLabel: { interval: 0, rotate: 0, fontSize: 12, color: '#6c6a64', fontFamily: 'Inter, sans-serif' },
          axisLine: { lineStyle: { color: '#e6dfd8', width: 1 } },
          axisTick: { show: false }
        },
        series: [{
          name: '特征重要性',
          type: 'bar',
          data: importances,
          barWidth: '50%',
          itemStyle: {
            color: function(params) {
              const colors = ['#cc785c', '#5db8a6', '#e8a55a', '#d4918a', '#7d8c80', '#8a9a5b', '#a0988a', '#c4a882']
              return colors[params.dataIndex % colors.length]
            },
            borderRadius: [0, 6, 6, 0],
            shadowBlur: 4,
            shadowColor: 'rgba(20,20,19,0.10)'
          },
          label: {
            show: true, position: 'right',
            formatter: function(p) { return p.value.toFixed(4); },
            fontSize: 11, color: '#6c6a64', fontWeight: 500
          },
          emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(20,20,19,0.25)' } }
        }]
      }
      
      featureChartInstance.setOption(option)
    }

    const calculateMetrics = (predictions) => {
      if (!predictions || predictions.length === 0) return
      
      const predicted = predictions.map(item => parseFloat(item.predictedSales || item.predicted_sales || 0))
      const actual = predictions.map(item => parseFloat(item.actualSales || item.actual_sales || 0))
      const errors = predictions.map(item => parseFloat(item.error || 0))
      const relativeErrors = predictions.map(item => parseFloat(item.relativeError || item.relative_error || 0))
      
      const mse = errors.reduce((sum, e) => sum + e * e, 0) / errors.length
      metrics.value.rmse = Math.sqrt(mse)
      
      metrics.value.mae = errors.reduce((sum, e) => sum + e, 0) / errors.length
      
      const actualMean = actual.reduce((sum, a) => sum + a, 0) / actual.length
      const ssRes = errors.reduce((sum, e) => sum + e * e, 0)
      const ssTot = actual.reduce((sum, a) => sum + Math.pow(a - actualMean, 2), 0)
      metrics.value.r2 = ssTot > 0 ? 1 - (ssRes / ssTot) : 0
      
      metrics.value.avgRelativeError = relativeErrors.length > 0 
        ? relativeErrors.reduce((sum, e) => sum + e, 0) / relativeErrors.length 
        : 0
      
      metrics.value.sampleCount = predictions.length
    }

    const initChart = async () => {
      try {
        const response = await request.get('/prediction/random-forest')
        if (response.code === 200 && response.data) {
          const predictions = response.data.predictions || []
          const features = response.data.featureImportance || []
          const responseMetrics = response.data.metrics || {}
          
          if (predictions.length > 0) {
            initPredictionChart(predictions)
            if (responseMetrics.rmse !== undefined) {
              metrics.value = {
                rmse: responseMetrics.rmse,
                mae: responseMetrics.mae,
                r2: responseMetrics.r2,
                avgRelativeError: responseMetrics.avgRelativeError,
                sampleCount: responseMetrics.sampleCount || predictions.length,
                targetType: responseMetrics.targetType || '销售数量/金额'
              }
            } else {
              calculateMetrics(predictions)
            }
          } else {
            predictionChartRef.value && (predictionChartInstance = echarts.init(predictionChartRef.value)).setOption({
              title: { text: '暂无数据', left: 'center', top: 'middle', textStyle: { fontSize: 16, color: '#8e8b82', fontFamily: 'Inter, sans-serif' } }
            })
          }
          
          if (features.length > 0) {
            initFeatureChart(features)
          } else {
            featureChartRef.value && (featureChartInstance = echarts.init(featureChartRef.value)).setOption({
              title: { text: '暂无数据', left: 'center', top: 'middle', textStyle: { fontSize: 16, color: '#8e8b82', fontFamily: 'Inter, sans-serif' } }
            })
          }
        }
      } catch (error) {
        console.error('加载预测数据失败:', error)
        if (predictionChartRef.value) {
          predictionChartInstance = echarts.init(predictionChartRef.value)
          predictionChartInstance.setOption({
            title: { text: '数据加载失败', left: 'center', top: 'middle', textStyle: { fontSize: 16, color: '#c64545', fontFamily: 'Inter, sans-serif' } }
          })
        }
        if (featureChartRef.value) {
          featureChartInstance = echarts.init(featureChartRef.value)
          featureChartInstance.setOption({
            title: { text: '数据加载失败', left: 'center', top: 'middle', textStyle: { fontSize: 16, color: '#c64545', fontFamily: 'Inter, sans-serif' } }
          })
        }
      }
    }

    onMounted(() => {
      initChart()
      window.addEventListener('resize', () => {
        if (predictionChartInstance) {
          predictionChartInstance.resize()
        }
        if (featureChartInstance) {
          featureChartInstance.resize()
        }
      })
    })

    onBeforeUnmount(() => {
      if (predictionChartInstance) {
        predictionChartInstance.dispose()
      }
      if (featureChartInstance) {
        featureChartInstance.dispose()
      }
    })

    return {
      predictionChartRef,
      featureChartRef,
      metrics,
      getMetricType
    }
  }
}
</script>

<style scoped>
.chart-card {
  background-color: #faf9f5;
  border: 1px solid #e6dfd8;
  border-radius: 12px;
}

.chart-card :deep(.el-card__header) {
  background-color: #faf9f5;
  border-bottom: 1px solid #ebe6df;
  padding: 20px 24px;
}

.chart-card :deep(.el-card__body) {
  padding: 20px 24px;
}

.card-title {
  font-size: 16px;
  font-weight: 500;
  color: #141413;
  font-family: 'Inter', sans-serif;
}

:deep(.el-descriptions__label) {
  font-weight: 500;
  color: #6c6a64;
  font-size: 13px;
}

:deep(.el-descriptions__content) {
  color: #141413;
}

:deep(.el-descriptions) {
  border-color: #e6dfd8;
}
</style>

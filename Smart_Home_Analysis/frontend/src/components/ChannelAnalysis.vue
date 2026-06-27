<template>
  <div ref="chartRef" style="width: 100%; height: 400px;"></div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import request from '../utils/request'

export default {
  name: 'ChannelAnalysis',
  setup() {
    const chartRef = ref(null)
    let chartInstance = null

    const initChart = async () => {
      if (!chartRef.value) return
      
      chartInstance = echarts.init(chartRef.value)
      
      try {
        const response = await request.get('/product/brands')
        const data = response.data || []
        
        const brands = data.map(item => item.brand)
        const sales = data.map(item => item.totalSales || item.total_sales)
        
        const option = {
          tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' },
            backgroundColor: '#181715',
            borderColor: '#252320',
            padding: [10, 14],
            textStyle: { color: '#faf9f5', fontSize: 13, fontFamily: 'Inter, sans-serif' }
          },
          grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
          xAxis: {
            type: 'category',
            data: brands,
            axisLabel: { rotate: 45, fontSize: 12, color: '#6c6a64', fontFamily: 'Inter, sans-serif' },
            axisLine: { lineStyle: { color: '#e6dfd8' } },
            axisTick: { show: false }
          },
          yAxis: {
            type: 'value',
            axisLabel: { fontSize: 12, color: '#6c6a64', fontFamily: 'Inter, sans-serif' },
            splitLine: { lineStyle: { color: '#e6dfd8', type: 'dashed' } }
          },
          series: [{
            name: '销售额',
            type: 'bar',
            data: sales,
            barWidth: '50%',
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#d4918a' },
                { offset: 0.5, color: '#cc785c' },
                { offset: 1, color: '#a9583e' }
              ]),
              borderRadius: [6, 6, 0, 0]
            },
            emphasis: {
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#cc785c' },
                  { offset: 0.7, color: '#cc785c' },
                  { offset: 1, color: '#d4918a' }
                ])
              }
            }
          }]
        }
        
        chartInstance.setOption(option)
      } catch (error) {
        console.error('加载渠道数据失败:', error)
        const option = {
          backgroundColor: 'transparent',
          tooltip: { trigger: 'axis', backgroundColor: '#181715', borderColor: '#252320', padding: [10, 14], textStyle: { color: '#faf9f5', fontSize: 13 } },
          grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
          xAxis: { type: 'category', data: ['线上商城', '实体店', '第三方平台', '官方旗舰店', '代理商'], axisLabel: { fontSize: 12, color: '#6c6a64' }, axisTick: { show: false } },
          yAxis: { type: 'value', axisLabel: { fontSize: 12, color: '#6c6a64' }, splitLine: { lineStyle: { color: '#e6dfd8', type: 'dashed' } } },
          series: [{
            data: [120, 200, 150, 80, 70],
            type: 'bar',
            barWidth: '50%',
            itemStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: '#d4918a' }, { offset: 0.5, color: '#cc785c' }, { offset: 1, color: '#a9583e' }]), borderRadius: [6, 6, 0, 0] }
          }]
        }
        chartInstance.setOption(option)
      }
    }

    onMounted(() => {
      initChart()
      window.addEventListener('resize', () => {
        if (chartInstance) {
          chartInstance.resize()
        }
      })
    })

    onBeforeUnmount(() => {
      if (chartInstance) {
        chartInstance.dispose()
      }
    })

    return {
      chartRef
    }
  }
}
</script>




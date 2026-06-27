<template>
  <div ref="chartRef" style="width: 100%; height: 550px;"></div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import request from '../utils/request'

export default {
  name: 'ProductAnalysis',
  setup() {
    const chartRef = ref(null)
    let chartInstance = null

    const initChart = async () => {
      if (!chartRef.value) return
      
      chartInstance = echarts.init(chartRef.value)
      
      try {
        const response = await request.get('/analysis/product')
        const data = response.data?.category || []
        
        if (!data || data.length === 0) {
          chartInstance.setOption({
            title: { text: '暂无数据', left: 'center', top: 'middle', textStyle: { fontSize: 16, color: '#8e8b82', fontFamily: 'Inter, sans-serif' } }
          })
          return
        }
        
        const chartData = data.map(item => ({
          value: item.totalSales || item.total_sales,
          name: item.category === '0' || item.category === 0 ? '其他' : item.category
        }))
        
        const option = {
          backgroundColor: 'transparent',
          title: {
            text: '产品品类销售占比',
            left: 'center',
            top: 0,
            textStyle: { fontSize: 18, fontWeight: 500, color: '#141413', fontFamily: 'Cormorant Garamond, EB Garamond, Times New Roman, serif' }
          },
          tooltip: {
            trigger: 'item',
            backgroundColor: '#181715',
            borderColor: '#252320',
            borderWidth: 1,
            padding: [12, 16],
            textStyle: { color: '#faf9f5', fontSize: 13, fontFamily: 'Inter, sans-serif' },
            formatter: '{b}: ¥{c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            top: 'middle',
            textStyle: { fontSize: 13, color: '#6c6a64', fontFamily: 'Inter, sans-serif' },
            itemGap: 14
          },
          series: [
            {
              name: '产品品类',
              type: 'pie',
              radius: ['40%', '70%'],
              center: ['55%', '55%'],
              avoidLabelOverlap: false,
              itemStyle: {
                borderRadius: 8,
                borderColor: '#faf9f5',
                borderWidth: 2,
                shadowBlur: 4,
                shadowColor: 'rgba(20,20,19,0.10)'
              },
              label: { show: true, formatter: '{b}\n{d}%', fontSize: 12, fontWeight: 500, color: '#3d3d3a', fontFamily: 'Inter, sans-serif' },
              labelLine: { show: true, length: 20, length2: 15, lineStyle: { width: 2 } },
              emphasis: {
                label: { show: true, fontSize: 16, fontWeight: 500, color: '#141413' },
                itemStyle: { shadowBlur: 16, shadowOffsetX: 0, shadowColor: 'rgba(20,20,19,0.25)', borderWidth: 3 }
              },
              data: chartData,
              color: ['#cc785c', '#5db8a6', '#e8a55a', '#d4918a', '#7d8c80', '#8a9a5b', '#a0988a', '#b58b6d', '#c4a882', '#9ab5a8', '#e0b5a1', '#cfc5b5']
            }
          ]
        }
        
        chartInstance.setOption(option)
      } catch (error) {
        console.error('加载产品数据失败:', error)
        chartInstance.setOption({
          title: {
            text: '数据加载失败',
            left: 'center',
            top: 'middle',
            textStyle: {
              fontSize: 16,
              color: '#F56C6C'
            }
          }
        })
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

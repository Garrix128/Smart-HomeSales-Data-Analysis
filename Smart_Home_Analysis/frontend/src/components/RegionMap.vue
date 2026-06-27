<template>
  <div ref="chartRef" style="width: 100%; height: 550px;"></div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import request from '../utils/request'

export default {
  name: 'RegionMap',
  setup() {
    const chartRef = ref(null)
    let chartInstance = null

    const initChart = async () => {
      if (!chartRef.value) return
      
      chartInstance = echarts.init(chartRef.value)
      
      try {
        const response = await request.get('/analysis/region')
        if (response.code === 200 && response.data) {
          const data = response.data
          
          if (!data || data.length === 0) {
            chartInstance.setOption({
              title: { text: '暂无数据', left: 'center', top: 'middle', textStyle: { fontSize: 16, color: '#8e8b82', fontFamily: 'Inter, sans-serif' } }
            })
            return
          }
          
          const regions = data.map(item => item.region || item.地区 || '未知')
          const sales = data.map(item => 
            parseFloat(item.totalSales || item.total_sales || item.总销售额 || 0)
          )
          
          const option = {
            backgroundColor: 'transparent',
            tooltip: {
              trigger: 'axis',
              axisPointer: { type: 'shadow' },
              backgroundColor: '#181715',
              borderColor: '#252320',
              borderWidth: 1,
              padding: [12, 16],
              textStyle: { color: '#faf9f5', fontSize: 13, fontFamily: 'Inter, sans-serif' },
              formatter: function(params) {
                const data = params[0]
                return `<div style="font-weight:500;margin-bottom:8px;color:#a09d96;font-size:12px;letter-spacing:1px;text-transform:uppercase;">${data.name}</div>
                        <div style="font-size:14px;">销售额: <span style="font-weight:500;color:#cc785c;">¥${data.value.toLocaleString()}</span></div>`
              }
            },
            grid: { left: '3%', right: '4%', bottom: '3%', top: '10%', containLabel: true },
            xAxis: {
              type: 'category',
              data: regions,
              axisLabel: { rotate: 0, interval: 0, fontSize: 12, color: '#6c6a64', fontFamily: 'Inter, sans-serif' },
              axisLine: { lineStyle: { color: '#e6dfd8', width: 1 } },
              axisTick: { show: false }
            },
            yAxis: {
              type: 'value',
              name: '销售额',
              axisLabel: {
                formatter: function(v) { return v >= 10000 ? (v / 10000).toFixed(1) + '万' : v.toLocaleString(); },
                fontSize: 12,
                color: '#6c6a64',
                fontFamily: 'Inter, sans-serif'
              },
              axisLine: { show: true, lineStyle: { color: '#cc785c', width: 2 } },
              nameTextStyle: { color: '#6c6a64', fontSize: 12 },
              splitLine: { lineStyle: { color: '#e6dfd8', type: 'dashed', width: 1 } }
            },
            series: [
              {
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
                  borderRadius: [6, 6, 0, 0],
                  shadowBlur: 4,
                  shadowColor: 'rgba(204,120,92,0.25)'
                },
                emphasis: {
                  itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                      { offset: 0, color: '#cc785c' },
                      { offset: 0.7, color: '#cc785c' },
                      { offset: 1, color: '#d4918a' }
                    ]),
                    shadowBlur: 10,
                    shadowColor: 'rgba(204,120,92,0.4)'
                  }
                },
                label: {
                  show: true,
                  position: 'top',
                  formatter: function(p) { return p.value >= 10000 ? (p.value / 10000).toFixed(1) + '万' : p.value.toLocaleString(); },
                  fontSize: 11,
                  color: '#6c6a64',
                  fontWeight: 500
                }
              }
            ]
          }
          
          chartInstance.setOption(option)
        } else {
          throw new Error('数据格式错误')
        }
      } catch (error) {
        console.error('加载地域数据失败:', error)
        chartInstance.setOption({
          title: { text: '数据加载失败', left: 'center', top: 'middle', textStyle: { fontSize: 16, color: '#c64545', fontFamily: 'Inter, sans-serif' } }
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

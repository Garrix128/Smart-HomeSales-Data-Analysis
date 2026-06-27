<template>
  <div ref="chartRef" style="width: 100%; height: 550px;"></div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import request from '../utils/request'

export default {
  name: 'SalesTrendChart',
  setup() {
    const chartRef = ref(null)
    let chartInstance = null

    const initChart = async () => {
      if (!chartRef.value) return
      
      chartInstance = echarts.init(chartRef.value)
      
      try {
        const response = await request.get('/sales/trend')
        const data = response.data || []
        
        if (!data || data.length === 0) {
          chartInstance.setOption({
            title: {
              text: '暂无数据',
              left: 'center',
              top: 'middle',
              textStyle: { fontSize: 16, color: '#8e8b82', fontFamily: 'Inter, sans-serif' }
            }
          })
          return
        }
        
        const dates = data.map(item => item.month || item.salesDate || item.sale_date)
        const sales = data.map(item => parseFloat(item.totalSales || item.total_sales || 0))
        const orders = data.map(item => parseFloat(item.orderCount || item.order_count || 0))
        
        const option = {
          backgroundColor: 'transparent',
          tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'cross', crossStyle: { color: '#8e8b82' }, lineStyle: { type: 'dashed' } },
            backgroundColor: '#181715',
            borderColor: '#252320',
            borderWidth: 1,
            padding: [12, 16],
            textStyle: { color: '#faf9f5', fontSize: 13, fontFamily: 'Inter, sans-serif' },
            formatter: function(params) {
              let result = `<div style="font-weight:500;margin-bottom:8px;color:#a09d96;font-size:12px;letter-spacing:1px;text-transform:uppercase;">${params[0].axisValue}</div>`
              params.forEach(param => {
                const value = param.seriesName === '销售额'
                  ? `¥${param.value.toLocaleString()}`
                  : param.value.toLocaleString()
                result += `<div style="margin:4px 0;font-size:14px;">${param.marker}${param.seriesName}: <span style="font-weight:500;">${value}</span></div>`
              })
              return result
            }
          },
          legend: {
            data: ['销售额', '订单数'],
            top: 0,
            textStyle: { fontSize: 13, color: '#6c6a64', fontFamily: 'Inter, sans-serif' },
            itemGap: 32
          },
          grid: { left: '3%', right: '4%', bottom: '12%', top: '12%', containLabel: true },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: dates,
            axisLabel: { rotate: 45, interval: 0, fontSize: 12, color: '#6c6a64', margin: 12, fontFamily: 'Inter, sans-serif' },
            axisLine: { lineStyle: { color: '#e6dfd8', width: 1 } },
            axisTick: { show: false }
          },
          yAxis: [
            {
              type: 'value',
              name: '销售额',
              position: 'left',
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
            {
              type: 'value',
              name: '订单数',
              position: 'right',
              axisLabel: { formatter: '{value}', fontSize: 12, color: '#6c6a64', fontFamily: 'Inter, sans-serif' },
              axisLine: { show: true, lineStyle: { color: '#5db8a6', width: 2 } },
              nameTextStyle: { color: '#6c6a64', fontSize: 12 },
              splitLine: { show: false }
            }
          ],
          series: [
            {
              name: '销售额',
              type: 'line',
              smooth: true,
              data: sales,
              itemStyle: { color: '#cc785c' },
              lineStyle: { width: 3, shadowColor: 'rgba(204,120,92,0.25)', shadowBlur: 6 },
              areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: 'rgba(204,120,92,0.25)' },
                  { offset: 0.5, color: 'rgba(204,120,92,0.08)' },
                  { offset: 1, color: 'rgba(204,120,92,0.0)' }
                ])
              },
              symbol: 'circle',
              symbolSize: 7,
              emphasis: { focus: 'series', itemStyle: { borderColor: '#faf9f5', borderWidth: 2, shadowBlur: 10, shadowColor: 'rgba(204,120,92,0.4)' } }
            },
            {
              name: '订单数',
              type: 'line',
              smooth: true,
              yAxisIndex: 1,
              data: orders,
              itemStyle: { color: '#5db8a6' },
              lineStyle: { width: 3, shadowColor: 'rgba(93,184,166,0.3)', shadowBlur: 6 },
              symbol: 'circle',
              symbolSize: 7,
              emphasis: { focus: 'series', itemStyle: { borderColor: '#faf9f5', borderWidth: 2, shadowBlur: 10, shadowColor: 'rgba(93,184,166,0.4)' } }
            }
          ]
        }
        
        chartInstance.setOption(option)
      } catch (error) {
        console.error('加载销售趋势数据失败:', error)
        chartInstance.setOption({
          title: {
            text: '数据加载失败',
            left: 'center',
            top: 'middle',
            textStyle: { fontSize: 16, color: '#c64545', fontFamily: 'Inter, sans-serif' }
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

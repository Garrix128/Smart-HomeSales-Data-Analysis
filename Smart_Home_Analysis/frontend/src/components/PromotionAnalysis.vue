<template>
  <div ref="chartRef" style="width: 100%; height: 550px;"></div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import request from '../utils/request'

export default {
  name: 'PromotionAnalysis',
  setup() {
    const chartRef = ref(null)
    let chartInstance = null

    const initChart = async () => {
      if (!chartRef.value) return
      
      chartInstance = echarts.init(chartRef.value)
      
      try {
        const response = await request.get('/analysis/promotion')
        if (response.code === 200 && response.data) {
          const data = response.data
          
          if (!data || data.length === 0) {
            chartInstance.setOption({
              title: {
                text: '暂无数据',
                left: 'center',
                top: 'middle',
                textStyle: {
                  fontSize: 16,
                  color: '#909399'
                }
              }
            })
            return
          }
          
          const promotionTypes = data.map(item => item.promotionType || item.promotion_type || '无促销')
          const sales = data.map(item => 
            parseFloat(item.totalSales || item.total_sales || 0)
          )
          const discountRates = data.map(item => 
            parseFloat(item.avgDiscountRate || item.avg_discount_rate || 0) * 100
          )
          
          const option = {
            backgroundColor: 'transparent',
            tooltip: {
              trigger: 'axis',
              axisPointer: { type: 'shadow' },
              backgroundColor: '#181715',
              borderColor: '#252320',
              padding: [12, 16],
              textStyle: { color: '#faf9f5', fontSize: 13, fontFamily: 'Inter, sans-serif' },
              formatter: function(params) {
                let result = `<div style="font-weight:500;margin-bottom:8px;color:#a09d96;font-size:12px;letter-spacing:1px;text-transform:uppercase;">${params[0].name}</div>`
                params.forEach(param => {
                  if (param.seriesName === '销售额') {
                    result += `<div style="margin:4px 0;font-size:14px;">${param.marker}${param.seriesName}: <span style="font-weight:500;color:#cc785c;">¥${param.value.toLocaleString()}</span></div>`
                  } else {
                    result += `<div style="margin:4px 0;font-size:14px;">${param.marker}${param.seriesName}: <span style="font-weight:500;color:#e8a55a;">${param.value.toFixed(2)}%</span></div>`
                  }
                })
                return result
              }
            },
            legend: {
              data: ['销售额', '平均折扣率'],
              top: 0,
              textStyle: { fontSize: 13, color: '#6c6a64', fontFamily: 'Inter, sans-serif' },
              itemGap: 32
            },
            grid: { left: '3%', right: '4%', bottom: '3%', top: '12%', containLabel: true },
            xAxis: {
              type: 'category',
              data: promotionTypes,
              axisLabel: { rotate: 0, interval: 0, fontSize: 12, color: '#6c6a64', fontFamily: 'Inter, sans-serif' },
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
                  fontSize: 12, color: '#6c6a64', fontFamily: 'Inter, sans-serif'
                },
                axisLine: { show: true, lineStyle: { color: '#cc785c', width: 2 } },
                nameTextStyle: { color: '#6c6a64', fontSize: 12 },
                splitLine: { lineStyle: { color: '#e6dfd8', type: 'dashed', width: 1 } }
              },
              {
                type: 'value',
                name: '折扣率 (%)',
                position: 'right',
                max: 100,
                axisLabel: { formatter: '{value}%', fontSize: 12, color: '#6c6a64', fontFamily: 'Inter, sans-serif' },
                axisLine: { show: true, lineStyle: { color: '#e8a55a', width: 2 } },
                nameTextStyle: { color: '#6c6a64', fontSize: 12 },
                splitLine: { show: false }
              }
            ],
            series: [
              {
                name: '销售额',
                type: 'bar',
                data: sales,
                barWidth: '50%',
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#d4918a' }, { offset: 0.5, color: '#cc785c' }, { offset: 1, color: '#a9583e' }
                  ]),
                  borderRadius: [6, 6, 0, 0],
                  shadowBlur: 4,
                  shadowColor: 'rgba(204,120,92,0.25)'
                },
                emphasis: {
                  itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                      { offset: 0, color: '#cc785c' }, { offset: 0.7, color: '#cc785c' }, { offset: 1, color: '#d4918a' }
                    ]),
                    shadowBlur: 10,
                    shadowColor: 'rgba(204,120,92,0.4)'
                  }
                },
                label: {
                  show: true, position: 'top',
                  formatter: function(p) { return p.value >= 10000 ? (p.value / 10000).toFixed(1) + '万' : p.value.toLocaleString(); },
                  fontSize: 11, color: '#6c6a64', fontWeight: 500
                }
              },
              {
                name: '平均折扣率',
                type: 'line',
                yAxisIndex: 1,
                data: discountRates,
                itemStyle: { color: '#e8a55a' },
                lineStyle: { width: 3, shadowBlur: 5, shadowColor: 'rgba(232,165,90,0.3)' },
                symbol: 'circle',
                symbolSize: 8,
                emphasis: {
                  focus: 'series',
                  itemStyle: { borderColor: '#faf9f5', borderWidth: 2, shadowBlur: 10, shadowColor: 'rgba(232,165,90,0.4)' }
                },
                label: { show: true, position: 'top', formatter: '{c}%', fontSize: 11, color: '#e8a55a', fontWeight: 500 }
              }
            ]
          }
          
          chartInstance.setOption(option)
        } else {
          throw new Error('数据格式错误')
        }
      } catch (error) {
        console.error('加载促销数据失败:', error)
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

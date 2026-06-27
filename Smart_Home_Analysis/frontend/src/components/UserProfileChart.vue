<template>
  <div class="user-profile-charts">
    <el-row :gutter="20">
      <el-col :span="12">
        <div ref="memberChartRef" style="width: 100%; height: 400px;"></div>
      </el-col>
      <el-col :span="12">
        <div ref="nonMemberChartRef" style="width: 100%; height: 400px;"></div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import request from '../utils/request'

export default {
  name: 'UserProfileChart',
  setup() {
    const memberChartRef = ref(null)
    const nonMemberChartRef = ref(null)
    let memberChartInstance = null
    let nonMemberChartInstance = null

    const initCharts = async () => {
      try {
        const response = await request.get('/user/member')
        
        if (response.code !== 200) {
          throw new Error(response.message || '获取数据失败')
        }
        
        const data = response.data || []
        
        if (!data || data.length === 0) {
          return
        }
        
        // 找到会员和非会员数据
        const memberData = data.find(item => {
          const type = String(item.member_type || '').trim()
          return type === '是' || type === '会员' || type === '1'
        })
        
        const nonMemberData = data.find(item => {
          const type = String(item.member_type || '').trim()
          return type === '否' || type === '非会员' || type === '0'
        })
        
        if (!memberData || !nonMemberData) {
          return
        }
        
        // 提取实际数据
        const memberUserCount = parseFloat(memberData.user_count || 0)
        const memberAvgConsumption = parseFloat(memberData.avg_consumption || 0)
        const memberTotalSales = parseFloat(memberData.total_sales || 0)
        
        const nonMemberUserCount = parseFloat(nonMemberData.user_count || 0)
        const nonMemberAvgConsumption = parseFloat(nonMemberData.avg_consumption || 0)
        const nonMemberTotalSales = parseFloat(nonMemberData.total_sales || 0)
        
        // 计算人均销售额
        const memberPerCapitaSales = memberUserCount > 0 ? memberTotalSales / memberUserCount : 0
        const nonMemberPerCapitaSales = nonMemberUserCount > 0 ? nonMemberTotalSales / nonMemberUserCount : 0
        
        // 计算平均值（作为基准）
        const avgUserCount = (memberUserCount + nonMemberUserCount) / 2
        const avgConsumption = (memberAvgConsumption + nonMemberAvgConsumption) / 2
        const avgTotalSales = (memberTotalSales + nonMemberTotalSales) / 2
        const avgPerCapitaSales = (memberPerCapitaSales + nonMemberPerCapitaSales) / 2
        
        // 计算总销售额占比
        const totalSales = memberTotalSales + nonMemberTotalSales
        const memberSalesRatio = totalSales > 0 ? (memberTotalSales / totalSales) * 100 : 50
        const nonMemberSalesRatio = totalSales > 0 ? (nonMemberTotalSales / totalSales) * 100 : 50
        
        // 计算相对指数（以平均值为100，放大差异）
        const calculateRelativeIndex = (value, avg) => {
          if (avg === 0) return 100
          const ratio = (value / avg) * 100
          return ratio
        }
        
        // 计算会员和非会员的指标值
        const memberValues = [
          calculateRelativeIndex(memberUserCount, avgUserCount),
          calculateRelativeIndex(memberAvgConsumption, avgConsumption),
          calculateRelativeIndex(memberTotalSales, avgTotalSales),
          calculateRelativeIndex(memberPerCapitaSales, avgPerCapitaSales),
          memberSalesRatio
        ]
        
        const nonMemberValues = [
          calculateRelativeIndex(nonMemberUserCount, avgUserCount),
          calculateRelativeIndex(nonMemberAvgConsumption, avgConsumption),
          calculateRelativeIndex(nonMemberTotalSales, avgTotalSales),
          calculateRelativeIndex(nonMemberPerCapitaSales, avgPerCapitaSales),
          nonMemberSalesRatio
        ]
        
        // 计算指标的最大值和最小值，用于设置雷达图范围
        const allValues = [...memberValues, ...nonMemberValues]
        const maxValue = Math.max(...allValues) * 1.1
        const minValue = Math.min(...allValues) * 0.9
        
        const indicators = [
          { name: '用户数量指数', max: Math.ceil(maxValue), min: Math.floor(minValue) },
          { name: '平均消费指数', max: Math.ceil(maxValue), min: Math.floor(minValue) },
          { name: '总销售额指数', max: Math.ceil(maxValue), min: Math.floor(minValue) },
          { name: '人均销售额指数', max: Math.ceil(maxValue), min: Math.floor(minValue) },
          { name: '销售额占比(%)', max: 100, min: 0 }
        ]
        
        // 会员图表配置
        if (memberChartRef.value) {
          memberChartInstance = echarts.init(memberChartRef.value)
          
          const memberOption = {
            backgroundColor: 'transparent',
            title: {
              text: '会员',
              left: 'center',
              top: 10,
              textStyle: { fontSize: 18, fontWeight: 500, color: '#cc785c', fontFamily: 'Cormorant Garamond, EB Garamond, Times New Roman, serif' }
            },
            tooltip: {
              trigger: 'item',
              backgroundColor: '#181715',
              borderColor: '#252320',
              borderWidth: 1,
              padding: [12, 16],
              textStyle: { color: '#faf9f5', fontSize: 13, fontFamily: 'Inter, sans-serif' },
              formatter: function(params) {
                let result = `<div style="font-weight:500;margin-bottom:8px;color:#cc785c;font-size:14px;">会员</div>`
                result += `<div style="margin:4px 0;color:#a09d96;font-size:11px;letter-spacing:1px;text-transform:uppercase;">实际数据</div>`
                result += `<div style="margin:2px 0;font-size:13px;">用户数: ${memberUserCount.toLocaleString()} 人</div>`
                result += `<div style="margin:2px 0;font-size:13px;">平均消费: ¥${memberAvgConsumption.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>`
                result += `<div style="margin:2px 0;font-size:13px;">总销售额: ¥${memberTotalSales.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>`
                result += `<div style="margin:2px 0;font-size:13px;">人均销售额: ¥${memberPerCapitaSales.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>`
                result += `<div style="margin:2px 0;font-size:13px;">销售额占比: ${memberSalesRatio.toFixed(2)}%</div>`
                return result
              }
            },
            radar: {
              indicator: indicators,
              center: ['50%', '55%'],
              radius: '70%',
              name: { textStyle: { color: '#6c6a64', fontSize: 12, fontWeight: 500, fontFamily: 'Inter, sans-serif' } },
              splitArea: {
                show: true,
                areaStyle: { color: ['rgba(204,120,92,0.03)', 'rgba(204,120,92,0.06)', 'rgba(204,120,92,0.09)', 'rgba(204,120,92,0.12)', 'rgba(204,120,92,0.15)'] }
              },
              splitLine: { lineStyle: { color: '#e6dfd8', width: 1.5, type: 'dashed' } },
              axisLine: { lineStyle: { color: '#e6dfd8', width: 2 } },
              splitNumber: 5
            },
            series: [{
              type: 'radar',
              data: [{
                value: memberValues,
                name: '会员',
                areaStyle: { color: 'rgba(204,120,92,0.35)' },
                itemStyle: { color: '#cc785c', borderWidth: 3, borderColor: '#faf9f5', shadowBlur: 5, shadowColor: 'rgba(204,120,92,0.25)' },
                lineStyle: { width: 4, color: '#cc785c', shadowBlur: 8, shadowColor: 'rgba(204,120,92,0.35)', type: 'solid' },
                symbol: 'circle',
                symbolSize: 10,
                label: { show: false }
              }],
              emphasis: {
                itemStyle: { shadowBlur: 16, shadowColor: 'rgba(20,20,19,0.25)', borderWidth: 4 },
                lineStyle: { width: 6 },
                areaStyle: { opacity: 0.6 }
              }
            }]
          }
          
          memberChartInstance.setOption(memberOption)
        }
        
        // 非会员图表配置
        if (nonMemberChartRef.value) {
          nonMemberChartInstance = echarts.init(nonMemberChartRef.value)
          
          const nonMemberOption = {
            backgroundColor: 'transparent',
            title: {
              text: '非会员',
              left: 'center',
              top: 10,
              textStyle: { fontSize: 18, fontWeight: 500, color: '#5db8a6', fontFamily: 'Cormorant Garamond, EB Garamond, Times New Roman, serif' }
            },
            tooltip: {
              trigger: 'item',
              backgroundColor: '#181715',
              borderColor: '#252320',
              borderWidth: 1,
              padding: [12, 16],
              textStyle: { color: '#faf9f5', fontSize: 13, fontFamily: 'Inter, sans-serif' },
              formatter: function(params) {
                let result = `<div style="font-weight:500;margin-bottom:8px;color:#5db8a6;font-size:14px;">非会员</div>`
                result += `<div style="margin:4px 0;color:#a09d96;font-size:11px;letter-spacing:1px;text-transform:uppercase;">实际数据</div>`
                result += `<div style="margin:2px 0;font-size:13px;">用户数: ${nonMemberUserCount.toLocaleString()} 人</div>`
                result += `<div style="margin:2px 0;font-size:13px;">平均消费: ¥${nonMemberAvgConsumption.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>`
                result += `<div style="margin:2px 0;font-size:13px;">总销售额: ¥${nonMemberTotalSales.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>`
                result += `<div style="margin:2px 0;font-size:13px;">人均销售额: ¥${nonMemberPerCapitaSales.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>`
                result += `<div style="margin:2px 0;font-size:13px;">销售额占比: ${nonMemberSalesRatio.toFixed(2)}%</div>`
                return result
              }
            },
            radar: {
              indicator: indicators,
              center: ['50%', '55%'],
              radius: '70%',
              name: { textStyle: { color: '#6c6a64', fontSize: 12, fontWeight: 500, fontFamily: 'Inter, sans-serif' } },
              splitArea: {
                show: true,
                areaStyle: { color: ['rgba(93,184,166,0.03)', 'rgba(93,184,166,0.06)', 'rgba(93,184,166,0.09)', 'rgba(93,184,166,0.12)', 'rgba(93,184,166,0.15)'] }
              },
              splitLine: { lineStyle: { color: '#e6dfd8', width: 1.5, type: 'dashed' } },
              axisLine: { lineStyle: { color: '#e6dfd8', width: 2 } },
              splitNumber: 5
            },
            series: [{
              type: 'radar',
              data: [{
                value: nonMemberValues,
                name: '非会员',
                areaStyle: { color: 'rgba(93,184,166,0.35)' },
                itemStyle: { color: '#5db8a6', borderWidth: 3, borderColor: '#faf9f5', shadowBlur: 5, shadowColor: 'rgba(93,184,166,0.25)' },
                lineStyle: { width: 4, color: '#5db8a6', shadowBlur: 8, shadowColor: 'rgba(93,184,166,0.35)', type: 'solid' },
                symbol: 'diamond',
                symbolSize: 10,
                label: { show: false }
              }],
              emphasis: {
                itemStyle: { shadowBlur: 16, shadowColor: 'rgba(20,20,19,0.25)', borderWidth: 4 },
                lineStyle: { width: 6 },
                areaStyle: { opacity: 0.6 }
              }
            }]
          }
          
          nonMemberChartInstance.setOption(nonMemberOption)
        }
      } catch (error) {
        console.error('加载用户数据失败:', error)
      }
    }

    onMounted(() => {
      initCharts()
      window.addEventListener('resize', () => {
        if (memberChartInstance) {
          memberChartInstance.resize()
        }
        if (nonMemberChartInstance) {
          nonMemberChartInstance.resize()
        }
      })
    })

    onBeforeUnmount(() => {
      if (memberChartInstance) {
        memberChartInstance.dispose()
      }
      if (nonMemberChartInstance) {
        nonMemberChartInstance.dispose()
      }
    })

    return {
      memberChartRef,
      nonMemberChartRef
    }
  }
}
</script>

<style scoped>
.user-profile-charts {
  width: 100%;
}
</style>

import axios from 'axios'

const service = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code !== 200) {
      const error = new Error(res.message || '请求失败')
      error.response = response
      return Promise.reject(error)
    }
    return res
  },
  error => {
    console.error('响应错误:', error)
    if (error.response && error.response.data) {
      const message = error.response.data.message || error.message || '请求失败'
      error.message = message
    }
    return Promise.reject(error)
  }
)

export default service


import axios from 'axios'
import { getToken, setToken } from '../stores/auth'

const api = axios.create({
  baseURL: '/api', // Im Dev über Vite-Proxy (/api -> Backend); SPA-Routen bleiben reloadbar
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use((config) => {
  const token = getToken()
  console.log('🔐 API Request Token:', token ? '✅ Present' : '❌ Missing', token ? token.substring(0, 20) + '...' : '')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (resp) => resp,
  (error) => {
    console.error('❌ API Error:', error.response?.status, error.response?.data || error.message)
    // If we get a 401 from the backend, clear token and redirect to login
    if (error?.response?.status === 401) {
      try { setToken(null) } catch {}
      if (typeof window !== 'undefined') {
        const current = window.location.pathname
        if (!current.startsWith('/login')) {
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default api

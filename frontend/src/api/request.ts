import axios, { type AxiosInstance, type AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'

// 自定义 Axios 实例类型，返回数据而不是完整响应
interface CustomAxiosInstance extends AxiosInstance {
    <T = any>(config: any): Promise<T>
    <T = any>(url: string, config?: any): Promise<T>
}

// 创建 axios 实例
const service = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
    timeout: 15000,
    headers: {
        'Content-Type': 'application/json',
    },
}) as CustomAxiosInstance

// 请求拦截器
service.interceptors.request.use(
    (config) => {
        // 添加 token (如果存在)
        const token = localStorage.getItem('access_token')
        if (token && config.headers) {
            config.headers.Authorization = `Bearer ${token}`
        }

        // 生成或传递 Request ID
        const requestId = crypto.randomUUID()
        if (config.headers) {
            config.headers['X-Request-ID'] = requestId
        }

        return config
    },
    (error) => {
        console.error('Request error:', error)
        return Promise.reject(error)
    }
)

// 响应拦截器
service.interceptors.response.use(
    (response: AxiosResponse) => {
        // 记录 Request ID (用于追踪)
        const requestId = response.headers['x-request-id']
        if (requestId) {
            console.log(`[${requestId}] Response received`)
        }

        return response.data
    },
    (error) => {
        // 统一错误处理
        const { response } = error

        if (response) {
            const { status, data } = response

            switch (status) {
                case 401:
                    ElMessage.error('未授权，请重新登录')
                    // 可以在这里跳转到登录页
                    break
                case 403:
                    ElMessage.error('拒绝访问')
                    break
                case 404:
                    ElMessage.error('请求的资源不存在')
                    break
                case 409:
                    ElMessage.error(data?.error?.message || '资源冲突')
                    break
                case 422:
                    ElMessage.error(data?.error?.message || '验证失败')
                    break
                case 500:
                    ElMessage.error('服务器错误')
                    break
                default:
                    ElMessage.error(data?.error?.message || '请求失败')
            }
        } else {
            ElMessage.error('网络错误，请检查网络连接')
        }

        return Promise.reject(error)
    }
)

export default service

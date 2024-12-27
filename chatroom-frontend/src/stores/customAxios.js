import axios from 'axios'

// const domain = 'https://your-domain.com'
const domain = 'http://127.0.0.1:8080' // dev

const customAxios = axios.create({
  baseURL: `${domain}/api`,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json'
  }
})

// 攔截器 request
customAxios.interceptors.request.use(
  function (config) {
    // 設置請求token
    const token = localStorage.getItem('access')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },

  function (error) {
    return Promise.reject(error)
  }
)

// 攔截器 response
customAxios.interceptors.response.use(
  function (response) {
    return response
  },

  function (error) {
    if (error.response) {
      switch (error.response.status) {
        case 400:
          console.log('資料有誤')
          break
        case 401:
          console.log('token無效拒絕存取')
          break
        case 404:
          console.log('沒頁面')
          break
        case 500:
          console.log('伺服器沒回應')
          break
        case 502:
          console.log('nginx閘道收到無效的回應')
          break
        default:
          console.log('ERROR不知道哪錯')
      }
    } else if (error.request) {
      console.log('Server無回應')
    } else {
      console.log('請求錯誤:', error.message)
    }
    return Promise.reject(error)
  }
)

export default customAxios

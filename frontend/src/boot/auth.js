import { defineBoot } from '#q-app'
import { api } from '@/boot/axios'

export default defineBoot(({ router }) => {
  api.interceptors.request.use(config => {
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      config.headers.Authorization = `Token ${storedToken}`
    }
    return config
  })

  api.interceptors.response.use(
    response => response,
    error => {
      if (error.response?.status === 401) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        router.push('/login')
      }
      return Promise.reject(error)
    }
  )
})

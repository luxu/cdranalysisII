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

  function getAuth() {
    const token = localStorage.getItem('token')
    const raw = localStorage.getItem('user')
    if (!token || !raw) return null
    try {
      return JSON.parse(raw)
    } catch {
      return null
    }
  }

  function getHome(user) {
    const groups = user.groups || []
    if (
      user.is_staff ||
      groups.includes('Administrador') ||
      groups.includes('Manager')
    ) {
      return '/admin'
    }
    return '/'
  }

  router.beforeEach((to, from, next) => {
    const user = getAuth()

    if (to.path === '/login') {
      if (user) {
        return next(getHome(user))
      }
      return next()
    }

    if (!user) {
      return next('/login')
    }

    if (
      to.matched.some(r => r.meta?.requiresAdmin) &&
      !user.groups?.includes('Administrador')
    ) {
      return next('/')
    }
    if (to.matched.some(r => r.meta?.requiresStaff)) {
      const groups = user.groups || []
      if (
        !user.is_staff &&
        !groups.includes('Administrador') &&
        !groups.includes('Manager')
      ) {
        return next('/')
      }
    }

    next()
  })
})

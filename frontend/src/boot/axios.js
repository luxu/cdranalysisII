import { defineBoot } from '#q-app'
import axios from 'axios'

// Instância única para acessar a API do backend (Django/DRF).
// Em dev, o proxy do Vite redireciona /api -> http://localhost:8000
const api = axios.create({ baseURL: '/api' })

// Normaliza o erro para exibição (Notify) nas páginas
api.interceptors.response.use(
  response => response,
  error => {
    error.friendlyMessage =
      error.response?.data?.detail ||
      error.response?.statusText ||
      error.message ||
      'Erro de comunicação com o servidor'
    return Promise.reject(error)
  }
)

export default defineBoot(({ app }) => {
  // Disponibiliza this.$axios e this.$api em componentes Options API
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api
})

export { api }

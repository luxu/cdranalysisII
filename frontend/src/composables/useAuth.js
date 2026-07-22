import { computed, ref } from 'vue'
import authService from '@/services/auth'

const user = ref(null)
const token = ref(localStorage.getItem('token') || null)

if (token.value) {
  const stored = localStorage.getItem('user')
  if (stored) {
    try {
      user.value = JSON.parse(stored)
    } catch {
      user.value = null
    }
  }
}

const isAuthenticated = computed(() => !!token.value)

const role = computed(() => {
  if (user.value?.is_staff) return 'admin'
  if (!user.value?.groups?.length) return null
  if (user.value.groups.includes('Administrador')) return 'admin'
  if (user.value.groups.includes('Manager')) return 'manager'
  return 'user'
})

const canAccessAdmin = computed(
  () => role.value === 'admin' || role.value === 'manager'
)

async function login(email, password) {
  const data = await authService.login(email, password)
  token.value = data.token
  user.value = data.user
  localStorage.setItem('token', data.token)
  localStorage.setItem('user', JSON.stringify(data.user))
  return data
}

function logout() {
  token.value = null
  user.value = null
  localStorage.removeItem('token')
  localStorage.removeItem('user')
}

export default function useAuth() {
  return { user, token, role, isAuthenticated, canAccessAdmin, login, logout }
}

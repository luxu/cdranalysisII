import { api } from '@/boot/axios'

const login = async (email, password) => {
  const { data } = await api.post('/auth/login/', { email, password })
  return data
}

export default { login }

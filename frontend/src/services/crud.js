import { api } from '@/boot/axios'

// Factory de serviço CRUD para um endpoint DRF ModelViewSet.
// list() aceita params de query (ex.: { page, page_size, search, ordering })
// e retorna o objeto paginado do DRF: { count, next, previous, results }
const createCrudService = endpoint => ({
  async list(params = {}) {
    const { data } = await api.get(endpoint, { params })
    return data
  },

  async get(id) {
    const { data } = await api.get(`${endpoint}${id}/`)
    return data
  },

  async create(payload) {
    const { data } = await api.post(endpoint, payload)
    return data
  },

  async update(id, payload) {
    const { data } = await api.put(`${endpoint}${id}/`, payload)
    return data
  },

  async remove(id) {
    await api.delete(`${endpoint}${id}/`)
  }
})

export default createCrudService

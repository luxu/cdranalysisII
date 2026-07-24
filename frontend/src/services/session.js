import { api } from '@/boot/axios'
import createCrudService from './crud'
import endpoints from './endpoints'

const sessionService = {
  ...createCrudService(endpoints.session),

  async dateRange() {
    const { data } = await api.get(`${endpoints.session}date_range/`)
    return data
  },

  async summaryByThing(params = {}) {
    const { data } = await api.get(`${endpoints.session}summary_by_thing/`, {
      params
    })
    return data
  }
}

export default sessionService

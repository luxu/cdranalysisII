import { reactive } from 'vue'

const state = reactive({
  search: '',
  statusAtivo: true,
  statusInativo: true,
  startDate: '',
  endDate: ''
})

export function useDashboardFilter() {
  function buildDeviceParams(thingId) {
    const params = { thing: thingId }

    if (state.search) {
      params.search = state.search
    }

    if (state.statusAtivo && !state.statusInativo) {
      params.status = true
    } else if (!state.statusAtivo && state.statusInativo) {
      params.status = false
    }

    return params
  }

  function buildSessionParams(thingId) {
    const params = { device__thing: thingId }

    if (state.startDate) {
      params.start_date = state.startDate
    }
    if (state.endDate) {
      params.end_date = state.endDate
    }

    return params
  }

  function clearDates() {
    state.startDate = ''
    state.endDate = ''
  }

  function setDefaultDates() {
    const now = new Date()
    const firstDay = new Date(now.getFullYear(), now.getMonth(), 1)
    const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0)
    state.startDate = firstDay.toISOString().split('T')[0]
    state.endDate = lastDay.toISOString().split('T')[0]
  }

  return {
    state,
    buildDeviceParams,
    buildSessionParams,
    clearDates,
    setDefaultDates
  }
}

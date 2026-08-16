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
    const y = now.getFullYear()
    const m = now.getMonth()
    const lastDay = new Date(y, m + 1, 0)
    const mm = String(m + 1).padStart(2, '0')
    state.startDate = `${y}-${mm}-01`
    state.endDate = `${y}-${mm}-${String(lastDay.getDate()).padStart(2, '0')}`
  }

  return {
    state,
    buildDeviceParams,
    buildSessionParams,
    clearDates,
    setDefaultDates
  }
}

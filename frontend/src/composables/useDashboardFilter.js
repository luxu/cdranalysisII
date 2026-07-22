import { reactive } from 'vue'

const state = reactive({
  search: '',
  statusAtivo: true,
  statusInativo: true
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

  return { state, buildDeviceParams }
}

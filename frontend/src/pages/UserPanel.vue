<template>
  <main class="flex-1 p-8 space-y-6 overflow-y-auto">
    <div v-if="loading" class="space-y-6">
      <div class="h-8 w-48 bg-slate-800 rounded animate-pulse" />
      <section class="flex flex-row gap-4">
        <div
          v-for="i in 3"
          :key="i"
          class="flex-1 bg-[#0D1321] border border-[#1E293B]/40 rounded-xl p-2.5 space-y-1.5 min-w-0"
        >
          <div class="h-2.5 w-16 bg-slate-800 rounded animate-pulse" />
          <div class="h-5 w-10 bg-slate-800 rounded animate-pulse" />
        </div>
      </section>
    </div>

    <template v-else-if="error">
      <div class="flex flex-col items-center justify-center py-20 text-center">
        <div class="bg-rose-500/10 text-rose-400 p-4 rounded-full mb-4">
          <svg
            class="w-8 h-8"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54-3.753 1.54-3.753 0-5.313l-6.928-12C5.86 4.087 5.86 4.087 4.3 6.375L1.464 9.5m16.5 0l-2.831 3.126M9 21h6"
            />
          </svg>
        </div>
        <p class="text-sm text-slate-400 max-w-xs">{{ error }}</p>
      </div>
    </template>

    <template v-else>
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-white tracking-tight">{{
            farmName
          }}</h1>
          <p class="text-xs text-slate-500 mt-1">Visão geral do cliente</p>
        </div>

        <div class="flex items-center gap-3">
          <q-input
            v-model="state.startDate"
            type="date"
            label="Data início"
            dense
            outlined
            dark
            class="w-36"
          />
          <q-input
            v-model="state.endDate"
            type="date"
            label="Data fim"
            dense
            outlined
            dark
            class="w-36"
          />
          <q-btn
            v-if="state.startDate || state.endDate"
            icon="clear"
            flat
            dense
            color="grey-5"
            @click="clearDates"
          />
        </div>
      </div>

      <section class="flex flex-row gap-4">
        <div
          class="flex-1 bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-4 shadow-sm min-w-0"
        >
          <div class="flex items-center justify-between mb-2">
            <span
              class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider truncate"
              >Total Devices</span
            >
            <div
              class="bg-[#10B981]/10 text-[#10B981] p-1.5 rounded-lg border border-[#10B981]/20 shrink-0 ml-2"
            >
              <svg
                class="w-3.5 h-3.5"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 5h10a2 2 0 012 2v10a2 2 0 01-2 2H7a2 2 0 01-2-2V7a2 2 0 012-2z"
                />
              </svg>
            </div>
          </div>
          <div>
            <span class="text-xl font-bold text-white">{{
              stats.totalDevices
            }}</span>
            <span class="text-[10px] text-slate-500 ml-1.5">devices</span>
          </div>
        </div>

        <div
          class="flex-1 bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-4 shadow-sm min-w-0"
        >
          <div class="flex items-center justify-between mb-2">
            <span
              class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider truncate"
              >Devices c/ Sessões</span
            >
            <div
              class="bg-[#3B82F6]/10 text-[#3B82F6] p-1.5 rounded-lg border border-[#3B82F6]/20 shrink-0 ml-2"
            >
              <svg
                class="w-3.5 h-3.5"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 5h10a2 2 0 012 2v10a2 2 0 01-2 2H7a2 2 0 01-2-2V7a2 2 0 012-2z"
                />
              </svg>
            </div>
          </div>
          <div>
            <span class="text-xl font-bold text-white">{{
              stats.devicesWithSessions
            }}</span>
            <span class="text-[10px] text-slate-500 ml-1.5">Sessões</span>
          </div>
        </div>

        <div
          class="flex-1 bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-4 shadow-sm min-w-0"
        >
          <div class="flex items-center justify-between mb-2">
            <span
              class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider truncate"
              >Total Real Usage</span
            >
            <div
              class="bg-[#F59E0B]/10 text-[#F59E0B] p-1.5 rounded-lg border border-[#F59E0B]/20 shrink-0 ml-2"
            >
              <svg
                class="w-3.5 h-3.5"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                />
              </svg>
            </div>
          </div>
          <div>
            <span class="text-xl font-bold text-white">{{
              stats.totalRealUsage
            }}</span>
            <span class="text-[10px] text-slate-500 ml-1.5">{{
              stats.uom
            }}</span>
          </div>
        </div>
      </section>
    </template>
  </main>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useDashboardFilter } from '@/composables/useDashboardFilter'
import deviceService from '@/services/device'
import sessionService from '@/services/session'
import profileService from '@/services/profile'

const {
  state,
  buildDeviceParams,
  buildSessionParams,
  clearDates,
  setDefaultDates
} = useDashboardFilter()

const loading = ref(true)
const error = ref(null)
const farmName = ref('')
const thingId = ref(null)

const stats = reactive({
  totalDevices: 0,
  devicesWithSessions: 0,
  totalRealUsage: '0',
  uom: 'MB'
})

async function fetchProfile() {
  const data = await profileService.get('me')
  thingId.value = data.thing
  farmName.value = data.thing_name || 'Cliente'
}

async function fetchFilteredDevices() {
  if (!thingId.value) {
    stats.totalDevices = 0
    return
  }
  const params = buildDeviceParams(thingId.value)
  params.page = 1
  params.page_size = 1
  const res = await deviceService.list(params)
  stats.totalDevices = res.count ?? 0
}

async function fetchSessionStats() {
  if (!thingId.value) {
    stats.devicesWithSessions = 0
    stats.totalRealUsage = '0'
    return
  }

  const params = buildSessionParams(thingId.value)
  const [devicesRes, usageRes] = await Promise.all([
    sessionService.topDevices(params),
    sessionService.usageByMonth(params)
  ])

  const totalSessions = devicesRes.reduce(
    (sum, d) => sum + (d.session_count || 0),
    0
  )
  const totalBytes = usageRes.reduce((sum, m) => sum + (m.total || 0), 0)

  stats.devicesWithSessions = devicesRes.length
  stats.totalRealUsage = (totalBytes / (1024 * 1024)).toFixed(2)
  stats.uom = 'MB'
}

watch(
  () => state.search,
  () => {
    fetchFilteredDevices()
  },
  { debounce: 300 }
)

watch(
  () => [state.statusAtivo, state.statusInativo],
  () => {
    fetchFilteredDevices()
  },
  { deep: true }
)

watch(
  () => [state.startDate, state.endDate],
  () => {
    fetchSessionStats()
  },
  { deep: true, debounce: 300 }
)

onMounted(async () => {
  try {
    setDefaultDates()
    await fetchProfile()
    await Promise.all([fetchFilteredDevices(), fetchSessionStats()])
  } catch (e) {
    error.value = e.friendlyMessage || 'Erro ao carregar dados'
  } finally {
    loading.value = false
  }
})
</script>

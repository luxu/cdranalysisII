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
      </div>

      <section class="flex flex-row gap-4">
        <div
          class="flex-1 bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-4 shadow-sm min-w-0"
        >
          <div class="flex items-center justify-between mb-2">
            <span
              class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider truncate"
              >Total de chips</span
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
                  d="M6 2h12l4 4v14a2 2 0 01-2 2H6a2 2 0 01-2-2V4a2 2 0 012-2z"
                />
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M8 6h2v4H8zm4 0h2v4h-2zm4 0h2v4h-2z"
                />
              </svg>
            </div>
          </div>
          <div>
            <span class="text-xl font-bold text-white">{{
              stats.totalDevices
            }}</span>
            <span class="text-[10px] text-slate-500 ml-1.5">chips</span>
          </div>
        </div>

        <div
          class="flex-1 bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-4 shadow-sm min-w-0"
        >
          <div class="flex items-center justify-between mb-2">
            <div>
              <span
                class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider truncate block"
                >Chips c/ Sessões</span
              >
              <span
                v-if="formatPeriod(state.startDate, state.endDate)"
                class="text-[9px] text-slate-500 mt-0.5 block"
              >
                {{ formatPeriod(state.startDate, state.endDate) }}
              </span>
            </div>
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
                  d="M6 2h12l4 4v14a2 2 0 01-2 2H6a2 2 0 01-2-2V4a2 2 0 012-2z"
                />
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M8 6h2v4H8zm4 0h2v4h-2zm4 0h2v4h-2z"
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
            <div>
              <span
                class="text-[9px] font-semibold text-slate-400 uppercase tracking-wider truncate block"
                >Consumo Total</span
              >
              <span
                v-if="formatPeriod(state.startDate, state.endDate)"
                class="text-[9px] text-slate-500 mt-0.5 block"
              >
                {{ formatPeriod(state.startDate, state.endDate) }}
              </span>
            </div>
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

      <section
        class="bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-5 shadow-sm space-y-4"
      >
        <div class="flex items-center justify-between mb-6">
          <h4 class="text-[7px] font-semibold text-white uppercase tracking-wider"
            >Consumo Mensal</h4
          >
          <span class="text-[10px] text-slate-500">últimos 12 meses</span>
        </div>

        <div v-if="chartLoading" class="h-52 flex items-center justify-center">
          <div
            class="w-6 h-6 border-2 border-[#10B981] border-t-transparent rounded-full animate-spin"
          />
        </div>

        <div
          v-else-if="monthlyUsage.length"
          class="relative"
        >
          <svg
            class="w-full"
            viewBox="0 0 600 240"
            preserveAspectRatio="xMidYMid meet"
          >
            <defs>
              <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#10B981" />
                <stop offset="100%" stop-color="#059669" />
              </linearGradient>
            </defs>

            <line
              x1="40"
              y1="200"
              x2="580"
              y2="200"
              stroke="#334155"
              stroke-width="1"
            />

            <line
              x1="40"
              y1="10"
              x2="40"
              y2="200"
              stroke="#334155"
              stroke-width="1"
            />

            <rect
              v-for="(d, i) in monthlyUsage"
              :key="i"
              :x="barX(i)"
              :y="barY(d.total)"
              :width="barW"
              :height="200 - barY(d.total)"
              rx="4"
              fill="url(#barGrad)"
            />

            <text
              v-for="(d, i) in monthlyUsage"
              :key="'l' + i"
              :x="barX(i) + barW / 2"
              y="218"
              text-anchor="middle"
              class="text-[9px] fill-slate-400"
              font-size="9"
            >
              {{ monthLabel(d.month) }}
            </text>

            <text
              v-for="(d, i) in monthlyUsage"
              :key="'v' + i"
              :x="barX(i) + barW / 2"
              :y="barY(d.total) - 4"
              text-anchor="middle"
              class="text-[5px] fill-white"
              font-size="5"
              font-weight="600"
            >
              {{ formatNumber(d.total) }}
            </text>
          </svg>
        </div>

        <div v-else class="h-52 flex items-center justify-center">
          <p class="text-xs text-slate-600">Nenhum dado de uso mensal</p>
        </div>
      </section>
    </template>
  </main>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useDashboardFilter } from '@/composables/useDashboardFilter'
import deviceService from '@/services/device'
import sessionService from '@/services/session'
import profileService from '@/services/profile'
import { formatNumber, formatPeriod } from '@/utils/format'

const {
  state,
  buildDeviceParams,
  buildSessionParams,
  clearDates,
  setDefaultDates
} = useDashboardFilter()

const loading = ref(true)
const chartLoading = ref(true)
const error = ref(null)
const farmName = ref('')
const thingId = ref(null)

const stats = reactive({
  totalDevices: 0,
  devicesWithSessions: 0,
  totalRealUsage: '0',
  uom: 'bytes'
})

const monthlyUsage = ref([])

const chartW = 600
const chartH = 200
const padLeft = 40
const padBottom = 40
const padTop = 10
const innerW = chartW - padLeft - 20
const innerH = chartH - padTop - padBottom

const barW = computed(() => {
  const count = monthlyUsage.value.length
  return count > 0 ? (innerW / count) * 0.45 : 0
})

const gap = computed(() => {
  const count = monthlyUsage.value.length
  return count > 0 ? (innerW / count) * 0.4 : 0
})

function barX(i) {
  const count = monthlyUsage.value.length
  if (count <= 0) return 0
  const step = innerW / count
  return padLeft + i * step + (step - barW.value) / 2
}

function barY(val) {
  const maxVal = Math.max(...monthlyUsage.value.map(d => d.total), 1)
  return padTop + innerH - (val / maxVal) * innerH
}

const monthNames = {
  '01': 'Jan',
  '02': 'Fev',
  '03': 'Mar',
  '04': 'Abr',
  '05': 'Mai',
  '06': 'Jun',
  '07': 'Jul',
  '08': 'Ago',
  '09': 'Set',
  10: 'Out',
  11: 'Nov',
  12: 'Dez'
}

const monthFullNames = {
  '01': 'Janeiro',
  '02': 'Fevereiro',
  '03': 'Março',
  '04': 'Abril',
  '05': 'Maio',
  '06': 'Junho',
  '07': 'Julho',
  '08': 'Agosto',
  '09': 'Setembro',
  10: 'Outubro',
  11: 'Novembro',
  12: 'Dezembro'
}

function monthLabel(monthStr) {
  const parts = monthStr.split('-')
  if (parts.length !== 2) return monthStr
  return `${monthNames[parts[1]] || parts[1]}/${parts[0].slice(2)}`
}

function monthFullLabel(monthStr) {
  const parts = monthStr.split('-')
  if (parts.length !== 2) return monthStr
  return `${monthFullNames[parts[1]] || parts[1]} ${parts[0]}`
}

async function fetchProfile() {
  try {
    const data = await profileService.get('me')
    thingId.value = data.thing
    farmName.value = data.thing_name || 'Cliente'
  } catch (error) {
    if (error.response?.status === 404) {
      thingId.value = null
      farmName.value = 'Visão Geral'
    } else {
      throw error
    }
  }
}

async function fetchFilteredDevices() {
  const params = thingId.value ? buildDeviceParams(thingId.value) : {}
  params.page = 1
  params.page_size = 1
  const res = await deviceService.list(params)
  stats.totalDevices = res.count ?? 0
}

async function fetchSessionStats() {
  const params = thingId.value ? buildSessionParams(thingId.value) : {}
  const [devicesRes, usageRes] = await Promise.all([
    sessionService.topDevices(params),
    sessionService.usageByMonth(params)
  ])

  const totalBytes = usageRes.reduce((sum, m) => sum + (m.total || 0), 0)

  stats.devicesWithSessions = devicesRes.length
  stats.totalRealUsage = formatNumber(totalBytes)
  stats.uom = 'Bytes'
}

async function fetchChartData() {
  chartLoading.value = true
  try {
    const params = thingId.value ? { device__thing: thingId.value } : {}
    const usageRes = await sessionService.usageByMonth(params)
    monthlyUsage.value = usageRes.filter(d => d.month).slice(-12)
  } catch {
    monthlyUsage.value = []
  } finally {
    chartLoading.value = false
  }
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
    await Promise.all([
      fetchFilteredDevices(),
      fetchSessionStats(),
      fetchChartData()
    ])
  } catch (e) {
    error.value = e.friendlyMessage || 'Erro ao carregar dados'
  } finally {
    loading.value = false
  }
})
</script>

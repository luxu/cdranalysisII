<template>
  <main class="flex-1 p-8 space-y-6 overflow-y-auto">
    <div v-if="loading" class="space-y-6">
      <div class="h-8 w-48 bg-slate-800 rounded animate-pulse" />
      <section class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div
          v-for="i in 3"
          :key="i"
          class="bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-6 space-y-3"
        >
          <div class="h-4 w-24 bg-slate-800 rounded animate-pulse" />
          <div class="h-8 w-16 bg-slate-800 rounded animate-pulse" />
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
          <p class="text-xs text-slate-500 mt-1">Painel da fazenda</p>
        </div>
      </div>

      <section class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div
          class="bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-6 shadow-sm space-y-3"
        >
          <div class="flex items-center justify-between">
            <span
              class="text-xs font-semibold text-slate-400 uppercase tracking-wider"
              >Total Devices</span
            >
            <div
              class="bg-[#10B981]/10 text-[#10B981] p-2 rounded-xl border border-[#10B981]/20"
            >
              <svg
                class="w-5 h-5"
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
            <span class="text-3xl font-bold text-white">{{
              stats.totalDevices
            }}</span>
            <span class="text-xs text-slate-500 ml-2">dispositivos</span>
          </div>
          <p class="text-[11px] text-slate-500"
            >Total de dispositivos da fazenda</p
          >
        </div>

        <div
          class="bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-6 shadow-sm space-y-3"
        >
          <div class="flex items-center justify-between">
            <span
              class="text-xs font-semibold text-slate-400 uppercase tracking-wider"
              >Devices com Sessions</span
            >
            <div
              class="bg-[#3B82F6]/10 text-[#3B82F6] p-2 rounded-xl border border-[#3B82F6]/20"
            >
              <svg
                class="w-5 h-5"
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
            <span class="text-3xl font-bold text-white">{{
              stats.devicesWithSessions
            }}</span>
            <span class="text-xs text-slate-500 ml-2">dispositivos</span>
          </div>
          <p class="text-[11px] text-slate-500"
            >Dispositivos que criaram ao menos uma sessão</p
          >
        </div>

        <div
          class="bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-6 shadow-sm space-y-3"
        >
          <div class="flex items-center justify-between">
            <span
              class="text-xs font-semibold text-slate-400 uppercase tracking-wider"
              >Total Real Usage</span
            >
            <div
              class="bg-[#F59E0B]/10 text-[#F59E0B] p-2 rounded-xl border border-[#F59E0B]/20"
            >
              <svg
                class="w-5 h-5"
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
            <span class="text-3xl font-bold text-white">{{
              stats.totalRealUsage
            }}</span>
            <span class="text-xs text-slate-500 ml-2">{{ stats.uom }}</span>
          </div>
          <p class="text-[11px] text-slate-500"
            >Soma total de uso de todas as sessões</p
          >
        </div>
      </section>

      <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div
          class="bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-5 shadow-sm space-y-4"
        >
          <div class="flex items-center justify-between">
            <h3
              class="text-xs font-semibold text-white uppercase tracking-wider"
              >Uso Mensal</h3
            >
            <span class="text-[10px] text-slate-500">bytes</span>
          </div>

          <div
            v-if="chartLoading"
            class="h-52 flex items-center justify-center"
          >
            <div
              class="w-6 h-6 border-2 border-[#10B981] border-t-transparent rounded-full animate-spin"
            />
          </div>

          <svg
            v-else-if="usageData.length"
            class="w-full"
            viewBox="0 0 400 180"
            preserveAspectRatio="xMidYMid meet"
          >
            <defs>
              <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#10B981" stop-opacity="0.35" />
                <stop offset="100%" stop-color="#10B981" stop-opacity="0.02" />
              </linearGradient>
            </defs>

            <polyline
              :points="linePoints"
              fill="none"
              stroke="#10B981"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />

            <polygon :points="areaPoints" fill="url(#areaGrad)" />

            <circle
              v-for="(p, i) in usageData"
              :key="i"
              :cx="xPos(i)"
              cy="yVal(p.total)"
              r="2.5"
              fill="#10B981"
              stroke="#0D1321"
              stroke-width="1.5"
            />

            <text
              v-for="(p, i) in usageLabels"
              :key="'l' + i"
              :x="xPos(i * step)"
              y="175"
              text-anchor="middle"
              class="text-[8px] fill-slate-500"
              font-size="7"
            >
              {{ p }}
            </text>
          </svg>

          <div v-else class="h-52 flex items-center justify-center">
            <p class="text-xs text-slate-600">Nenhum dado de uso mensal</p>
          </div>
        </div>

        <div
          class="bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-5 shadow-sm space-y-3"
        >
          <div class="flex items-center justify-between">
            <h3
              class="text-xs font-semibold text-white uppercase tracking-wider"
              >Top Devices</h3
            >
            <span class="text-[10px] text-slate-500">consumo total</span>
          </div>

          <div
            v-if="chartLoading"
            class="h-52 flex items-center justify-center"
          >
            <div
              class="w-6 h-6 border-2 border-[#3B82F6] border-t-transparent rounded-full animate-spin"
            />
          </div>

          <div v-else-if="topDevices.length" class="space-y-2.5">
            <div
              v-for="(d, i) in topDevices"
              :key="d.device_id"
              class="space-y-1"
            >
              <div class="flex items-center justify-between text-[11px]">
                <span class="text-slate-300 truncate max-w-[180px]">{{
                  d.label
                }}</span>
                <span class="text-slate-500 font-mono tabular-nums">{{
                  d.display
                }}</span>
              </div>
              <div class="h-1.5 bg-[#1E293B] rounded-full overflow-hidden">
                <div
                  class="h-full rounded-full transition-all duration-500"
                  :class="barColor(i)"
                  :style="{ width: d.pct + '%' }"
                />
              </div>
            </div>
          </div>

          <div v-else class="h-52 flex items-center justify-center">
            <p class="text-xs text-slate-600">Nenhum dado de consumo</p>
          </div>
        </div>
      </section>
    </template>
  </main>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useDashboardFilter } from '@/composables/useDashboardFilter'
import { api } from '@/boot/axios'
import deviceService from '@/services/device'
import sessionService from '@/services/session'
import profileService from '@/services/profile'

const { state, buildDeviceParams } = useDashboardFilter()

const loading = ref(true)
const chartLoading = ref(true)
const error = ref(null)
const farmName = ref('')
const thingId = ref(null)

const stats = reactive({
  totalDevices: 0,
  devicesWithSessions: 0,
  totalRealUsage: '0',
  uom: 'MB'
})

const usageData = ref([])
const topDevices = ref([])

const sessionCache = { devicesWithSessions: 0, totalRealUsage: '0', uom: 'MB' }

function formatBytes(bytes) {
  if (bytes >= 1073741824) return (bytes / 1073741824).toFixed(2) + ' GB'
  if (bytes >= 1048576) return (bytes / 1048576).toFixed(2) + ' MB'
  if (bytes >= 1024) return (bytes / 1024).toFixed(2) + ' KB'
  return bytes.toFixed(0) + ' B'
}

function formatBytesShort(bytes) {
  if (bytes >= 1073741824) return (bytes / 1073741824).toFixed(1) + ' GB'
  if (bytes >= 1048576) return (bytes / 1048576).toFixed(1) + ' MB'
  if (bytes >= 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return bytes.toFixed(0) + ' B'
}

const barColors = [
  'bg-[#10B981]',
  'bg-[#3B82F6]',
  'bg-[#F59E0B]',
  'bg-[#8B5CF6]',
  'bg-[#EC4899]',
  'bg-[#06B6D4]',
  'bg-[#F97316]',
  'bg-[#14B8A6]',
  'bg-[#6366F1]',
  'bg-[#D946EF]'
]

function barColor(i) {
  return barColors[i % barColors.length]
}

const padding = { top: 10, right: 10, bottom: 20, left: 5 }
const chartW = 400
const chartH = 180
const innerW = chartW - padding.left - padding.right
const innerH = chartH - padding.top - padding.bottom

function xPos(i) {
  const count = usageData.value.length
  if (count <= 1) return padding.left + innerW / 2
  return padding.left + (i / (count - 1)) * innerW
}

function yVal(v) {
  const maxVal = Math.max(...usageData.value.map(d => d.total), 1)
  return padding.top + innerH - (v / maxVal) * innerH
}

const linePoints = computed(() =>
  usageData.value.map((d, i) => `${xPos(i)},${yVal(d.total)}`).join(' ')
)

const areaPoints = computed(() => {
  if (!usageData.value.length) return ''
  const pts = usageData.value.map((d, i) => `${xPos(i)},${yVal(d.total)}`)
  const last = usageData.value.length - 1
  return `${pts.join(' ')} ${xPos(last)},${padding.top + innerH} ${xPos(0)},${padding.top + innerH}`
})

const step = computed(() => Math.max(1, Math.floor(usageData.value.length / 6)))

const usageLabels = computed(() => {
  if (!usageData.value.length) return []
  const labels = []
  for (let i = 0; i < usageData.value.length; i += step.value) {
    labels.push(usageData.value[i].month.slice(5))
  }
  return labels
})

async function fetchProfile() {
  const data = await profileService.get('me')
  thingId.value = data.thing
  farmName.value = data.thing_name || 'Fazenda'
}

async function fetchFilteredDevices() {
  if (!thingId.value) return
  const params = buildDeviceParams(thingId.value)
  params.page = 1
  params.page_size = 1
  const res = await deviceService.list(params)
  stats.totalDevices = res.count ?? 0
}

async function fetchSessionStats() {
  if (!thingId.value) return
  const firstPage = await sessionService.list({
    device__thing: thingId.value,
    page: 1
  })
  const deviceSet = new Set()
  let totalBytes = 0

  function process(results) {
    for (const s of results) {
      deviceSet.add(s.device)
      totalBytes += parseFloat(s.realusage) || 0
    }
  }

  process(firstPage.results)

  const totalPages = Math.ceil(firstPage.count / 50)
  const pagesToFetch = Math.min(totalPages, 10)

  for (let p = 2; p <= pagesToFetch; p++) {
    const res = await sessionService.list({
      device__thing: thingId.value,
      page: p
    })
    process(res.results)
  }

  sessionCache.devicesWithSessions = deviceSet.size
  sessionCache.totalRealUsage = (totalBytes / (1024 * 1024)).toFixed(2)
  sessionCache.uom = 'MB'

  stats.devicesWithSessions = sessionCache.devicesWithSessions
  stats.totalRealUsage = sessionCache.totalRealUsage
  stats.uom = sessionCache.uom
}

async function fetchCharts() {
  if (!thingId.value) return
  chartLoading.value = true
  try {
    const [usageRes, topRes] = await Promise.all([
      api.get('/api/sessions/usage_by_month/', {
        params: { device__thing: thingId.value }
      }),
      api.get('/api/sessions/top_devices/', {
        params: { device__thing: thingId.value }
      })
    ])

    usageData.value = usageRes.data.filter(d => d.month).slice(-12)

    topDevices.value = topRes.data.slice(0, 10).map(d => {
      const label = d.iccid || d.imsi || d.msisdn || d.device_id.slice(0, 8)
      return {
        ...d,
        label: label.length > 22 ? label.slice(0, 20) + '…' : label,
        display: formatBytesShort(d.total_bytes)
      }
    })

    const maxTop = Math.max(...topDevices.value.map(d => d.total_bytes), 1)
    for (const d of topDevices.value) {
      d.pct = (d.total_bytes / maxTop) * 100
    }
  } catch {
    usageData.value = []
    topDevices.value = []
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

onMounted(async () => {
  try {
    await fetchProfile()
    await Promise.all([
      fetchFilteredDevices(),
      fetchSessionStats(),
      fetchCharts()
    ])
  } catch (e) {
    error.value = e.friendlyMessage || 'Erro ao carregar dados'
  } finally {
    loading.value = false
  }
})
</script>

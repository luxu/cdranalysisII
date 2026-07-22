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
    </template>
  </main>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useDashboardFilter } from '@/composables/useDashboardFilter'
import deviceService from '@/services/device'
import sessionService from '@/services/session'
import profileService from '@/services/profile'

const { state, buildDeviceParams } = useDashboardFilter()

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

const sessionCache = { devicesWithSessions: 0, totalRealUsage: '0', uom: 'MB' }

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
    await Promise.all([fetchFilteredDevices(), fetchSessionStats()])
  } catch (e) {
    error.value = e.friendlyMessage || 'Erro ao carregar dados'
  } finally {
    loading.value = false
  }
})
</script>

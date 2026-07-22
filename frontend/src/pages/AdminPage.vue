<template>
  <main class="flex-1 p-8 space-y-6 overflow-y-auto">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-white tracking-tight">Admin</h1>
    </div>

    <section class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div
        class="bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-6 shadow-sm space-y-3"
      >
        <div class="flex items-center justify-between">
          <span
            class="text-xs font-semibold text-slate-400 uppercase tracking-wider"
            >Fazendas</span
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
                d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"
              />
            </svg>
          </div>
        </div>
        <div
          v-if="loading"
          class="h-8 w-16 bg-slate-800 rounded animate-pulse"
        />
        <div v-else>
          <span class="text-3xl font-bold text-white">{{
            stats.thingsCount
          }}</span>
          <span class="text-xs text-slate-500 ml-2">fazendas</span>
        </div>
        <p class="text-[11px] text-slate-500">Total de fazendas cadastradas</p>
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
        <div
          v-if="loading"
          class="h-8 w-16 bg-slate-800 rounded animate-pulse"
        />
        <div v-else>
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
        <div
          v-if="loading"
          class="h-8 w-24 bg-slate-800 rounded animate-pulse"
        />
        <div v-else>
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
  </main>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import thingService from '@/services/thing'
import sessionService from '@/services/session'

const loading = ref(true)
const stats = reactive({
  thingsCount: 0,
  devicesWithSessions: 0,
  totalRealUsage: '0',
  uom: 'MB'
})

async function fetchAllPages() {
  const firstPage = await sessionService.list({ page: 1 })
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
    const res = await sessionService.list({ page: p })
    process(res.results)
  }

  return {
    devicesWithSessions: deviceSet.size,
    totalRealUsage: (totalBytes / (1024 * 1024)).toFixed(2),
    uom: 'MB'
  }
}

onMounted(async () => {
  try {
    const [thingsRes, sessionStats] = await Promise.all([
      thingService.list({ page: 1 }),
      fetchAllPages()
    ])

    stats.thingsCount = thingsRes.count
    stats.devicesWithSessions = sessionStats.devicesWithSessions
    stats.totalRealUsage = sessionStats.totalRealUsage
    stats.uom = sessionStats.uom
  } catch {
    stats.thingsCount = 0
    stats.devicesWithSessions = 0
    stats.totalRealUsage = '0'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <main class="flex-1 p-8 space-y-6 overflow-y-auto">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-white tracking-tight">Admin</h1>
        <p v-if="dbDateRange.min_date" class="text-xs text-slate-400 mt-1">
          Base de dados: {{ dbDateRange.min_date }} a {{ dbDateRange.max_date }}
        </p>
      </div>
    </div>

    <div class="flex items-center gap-3 flex-wrap">
      <q-input
        v-model="startDate"
        dense
        outlined
        label="Data início"
        class="w-[160px]"
        readonly
      >
        <template v-slot:prepend>
          <q-icon name="event" class="cursor-pointer">
            <q-popup-proxy
              cover
              transition-show="scale"
              transition-hide="scale"
            >
              <q-date v-model="startDate" mask="YYYY-MM-DD" />
            </q-popup-proxy>
          </q-icon>
        </template>
      </q-input>
      <q-input
        v-model="endDate"
        dense
        outlined
        label="Data fim"
        class="w-[160px]"
        readonly
      >
        <template v-slot:prepend>
          <q-icon name="event" class="cursor-pointer">
            <q-popup-proxy
              cover
              transition-show="scale"
              transition-hide="scale"
            >
              <q-date v-model="endDate" mask="YYYY-MM-DD" />
            </q-popup-proxy>
          </q-icon>
        </template>
      </q-input>
      <q-btn
        flat
        dense
        color="grey"
        label="Limpar"
        icon="clear_all"
        @click="clearDates"
      />
    </div>

    <section class="flex gap-4 overflow-x-auto pb-2">
      <div
        v-for="org in sortedOrganizations"
        :key="org.thing_id"
        class="border rounded-2xl px-5 py-4 shrink-0 min-w-[180px] transition-all duration-200 hover:scale-105 cursor-pointer"
        :class="
          selectedThing?.id === org.thing_id
            ? 'border-[#10B981] bg-[#10B981]/5'
            : 'border-slate-600'
        "
        @click="selectThing(org)"
      >
        <p class="text-white font-bold uppercase text-sm mb-3 truncate">{{
          org.thing_name
        }}</p>
        <p class="text-slate-300 text-sm"
          >{{ org.device_count }}
          {{ org.device_count === 1 ? 'device' : 'devices' }}</p
        >
        <p class="text-slate-300 text-sm"
          >consumo {{ formatUsage(org.total_usage) }}</p
        >
      </div>
    </section>

    <Transition name="panel">
      <section
        v-if="selectedThing"
        class="bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl overflow-hidden"
      >
        <div
          class="px-5 py-3 border-b border-[#1E293B]/40 flex items-center justify-between"
        >
          <h3 class="text-sm font-bold text-white uppercase tracking-wider">
            Sessões — {{ selectedThing.name }}
          </h3>
          <span class="text-[11px] text-slate-500"
            >{{ sessionPagination.rowsNumber }} sessões</span
          >
        </div>
        <q-table
          v-model:pagination="sessionPagination"
          :rows="sessionRows"
          :columns="sessionColumns"
          row-key="id"
          :loading="sessionLoading"
          flat
          dense
          dark
          hide-bottom
          @request="fetchSessions"
        >
          <template v-slot:body-cell-realusage="props">
            <q-td :props="props" class="text-right font-mono tabular-nums">
              {{ formatUsage(parseFloat(props.value) || 0) }}
            </q-td>
          </template>
          <template v-slot:body-cell-sessioncreatetime="props">
            <q-td :props="props">
              {{ formatDate(props.value) }}
            </q-td>
          </template>
        </q-table>
        <div
          v-if="sessionPagination.rowsNumber > sessionPagination.rowsPerPage"
          class="flex items-center justify-center gap-2 py-3 border-t border-[#1E293B]/40"
        >
          <q-btn
            flat
            dense
            size="sm"
            color="grey"
            icon="chevron_left"
            :disable="sessionPagination.page <= 1"
            @click="changePage(sessionPagination.page - 1)"
          />
          <span class="text-xs text-slate-400">
            Página {{ sessionPagination.page }} de {{ totalPages }}
          </span>
          <q-btn
            flat
            dense
            size="sm"
            color="grey"
            icon="chevron_right"
            :disable="sessionPagination.page >= totalPages"
            @click="changePage(sessionPagination.page + 1)"
          />
        </div>
      </section>
    </Transition>
  </main>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import sessionService from '@/services/session'

const loading = ref(true)
const organizations = ref([])
const dbDateRange = ref({ min_date: null, max_date: null })

const selectedThing = ref(null)
const sessionRows = ref([])
const sessionLoading = ref(false)
const sessionPagination = ref({
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0
})

const sessionColumns = [
  {
    name: 'sessionid',
    label: 'Session ID',
    align: 'left',
    field: val => val.sessionid,
    sortable: true
  },
  {
    name: 'imsi',
    label: 'IMSI',
    align: 'left',
    field: val => val.imsi,
    sortable: true
  },
  {
    name: 'msisdn',
    label: 'MSISDN',
    align: 'left',
    field: val => val.msisdn,
    sortable: true
  },
  {
    name: 'sessioncreatetime',
    label: 'Data',
    align: 'left',
    field: val => val.sessioncreatetime,
    sortable: true
  },
  {
    name: 'realusage',
    label: 'Uso',
    align: 'right',
    field: val => val.realusage,
    sortable: true
  },
  {
    name: 'uom',
    label: 'UOM',
    align: 'left',
    field: val => val.uom,
    sortable: true
  }
]

function today() {
  return new Date().toISOString().slice(0, 10)
}

const startDate = ref(today())
const endDate = ref(today())

const totalPages = computed(() =>
  Math.ceil(
    sessionPagination.value.rowsNumber / sessionPagination.value.rowsPerPage
  )
)

const sortedOrganizations = computed(() =>
  [...organizations.value].sort((a, b) => b.device_count - a.device_count)
)

function formatUsage(bytes) {
  if (bytes >= 1073741824) return (bytes / 1073741824).toFixed(2) + ' GB'
  if (bytes >= 1048576) return (bytes / 1048576).toFixed(2) + ' MB'
  if (bytes >= 1024) return (bytes / 1024).toFixed(2) + ' KB'
  return bytes.toFixed(0) + ' B'
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('pt-BR')
}

async function fetchOrganizations() {
  const params = {}
  if (startDate.value) params.start_date = startDate.value
  if (endDate.value) params.end_date = endDate.value
  const res = await sessionService.summaryByThing(params)
  organizations.value = res
}

async function fetchSessions(props) {
  sessionLoading.value = true
  try {
    const params = {
      page: props.pagination.page,
      page_size: props.pagination.rowsPerPage
    }
    if (selectedThing.value) params.device__thing = selectedThing.value.id
    if (startDate.value) params.start_date = startDate.value
    if (endDate.value) params.end_date = endDate.value

    const data = await sessionService.list(params)
    sessionRows.value = data.results
    sessionPagination.value.page = props.pagination.page
    sessionPagination.value.rowsNumber = data.count
  } catch {
    sessionRows.value = []
  } finally {
    sessionLoading.value = false
  }
}

function changePage(page) {
  fetchSessions({ pagination: { ...sessionPagination.value, page } })
}

function selectThing(org) {
  if (selectedThing.value?.id === org.thing_id) {
    selectedThing.value = null
    sessionRows.value = []
    return
  }
  selectedThing.value = { id: org.thing_id, name: org.thing_name }
  sessionPagination.value.page = 1
  fetchSessions({
    pagination: { ...sessionPagination.value, page: 1 }
  })
}

function clearDates() {
  startDate.value = today()
  endDate.value = today()
}

watch([startDate, endDate], () => {
  fetchOrganizations()
  if (selectedThing.value) {
    sessionPagination.value.page = 1
    fetchSessions({
      pagination: { ...sessionPagination.value, page: 1 }
    })
  }
})

onMounted(async () => {
  try {
    const range = await sessionService.dateRange()
    dbDateRange.value = range
    if (range.min_date) startDate.value = range.min_date
    if (range.max_date) endDate.value = range.max_date
    await fetchOrganizations()
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.panel-enter-active {
  transition: all 0.3s ease-out;
}
.panel-enter-from {
  opacity: 0;
  transform: translateY(-8px);
}
.panel-leave-active {
  transition: all 0.2s ease-in;
}
.panel-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>

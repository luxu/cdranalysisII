<template>
  <main class="flex-1 p-8 space-y-6 overflow-y-auto">
    <!-- Cabeçalho e Data dos dados -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-white tracking-tight"
          >Administrador</h1
        >
        <p v-if="dbDateRange.min_date" class="text-xs text-slate-400 mt-1">
          Base de dados: {{ dbDateRange.min_date }} a {{ dbDateRange.max_date }}
        </p>
      </div>
    </div>
    <!-- fim Cabeçalho e Data dos dados -->

    <!-- Gráfico Top 10 Chips por Consumo -->
    <section
      v-if="topDevices.length"
      class="bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-5"
    >
      <h3 class="text-sm font-bold text-white uppercase tracking-wider mb-4">
        Top 10 Chips por Consumo
      </h3>
      <div class="space-y-2">
        <div
          v-for="device in topDevices"
          :key="device.device_id"
          class="flex items-center gap-3 cursor-pointer rounded-lg px-2 py-1 transition-all duration-200 hover:bg-[#1E293B]/50"
          :class="
            selectedDevice?.device_id === device.device_id
              ? 'bg-[#10B981]/10 border border-[#10B981]/30'
              : 'border border-transparent'
          "
          @click="selectDevice(device)"
        >
          <span
            class="text-xs text-slate-400 w-[140px] truncate font-mono"
            :title="device.iccid"
            >{{ device.iccid }}</span
          >
          <div class="flex-1 h-5 bg-slate-800 rounded overflow-hidden">
            <div
              class="h-full bg-[#10B981]/70 rounded transition-all duration-500"
              :style="{ width: devicePercent(device.total_bytes) + '%' }"
            />
          </div>
          <span
            class="text-xs text-slate-300 w-[80px] text-right font-mono tabular-nums"
            >{{ formatNumber(device.total_bytes) }}</span
          >
          <span class="text-[11px] text-slate-500 w-[70px] text-right"
            >{{ device.session_count }} sessões</span
          >
        </div>
      </div>
    </section>
    <!-- fim Gráfico Top 10 Chips por Consumo -->

    <!-- Filtros -->
    <div class="flex items-center gap-3 flex-wrap">
      <div class="q-pa-md" style="max-width: 300px">
        <q-input
          filled
          readonly
          :model-value="formatDate(startDate)"
          mask="##/##/####"
        >
          <template v-slot:append>
            <q-icon name="event" class="cursor-pointer">
              <q-popup-proxy
                cover
                transition-show="scale"
                transition-hide="scale"
              >
                <q-date
                  v-model="startDate"
                  mask="YYYY-MM-DD"
                  :locale="localeBR"
                >
                  <div class="row items-center justify-end">
                    <q-btn v-close-popup label="Close" color="primary" flat />
                  </div>
                </q-date>
              </q-popup-proxy>
            </q-icon>
          </template>
        </q-input>
      </div>

      <div class="q-pa-md" style="max-width: 300px">
        <q-input
          filled
          readonly
          :model-value="formatDate(endDate)"
          mask="##/##/####"
        >
          <template v-slot:append>
            <q-icon name="event" class="cursor-pointer">
              <q-popup-proxy
                cover
                transition-show="scale"
                transition-hide="scale"
              >
                <q-date v-model="endDate" mask="YYYY-MM-DD" :locale="localeBR">
                  <div class="row items-center justify-end">
                    <q-btn v-close-popup label="Close" color="primary" flat />
                  </div>
                </q-date>
              </q-popup-proxy>
            </q-icon>
          </template>
        </q-input>
      </div>

      <q-input
        v-model="realusageMin"
        dense
        outlined
        type="number"
        label="Uso mín"
        class="w-[120px]"
        debounce="300"
      />
      <q-input
        v-model="realusageMax"
        dense
        outlined
        type="number"
        label="Uso máx"
        class="w-[120px]"
        debounce="300"
      />
      <q-btn
        flat
        dense
        color="grey"
        label="Limpar"
        icon="clear_all"
        class="shrink-0 whitespace-nowrap"
        @click="clearDates"
      />
    </div>
    <!-- fim dos Filtros -->

    <!-- Cards dos Things(CLIENTES) -->
    <section class="flex gap-4 overflow-x-auto pb-2">
      <div
        v-for="thing in sortedThings"
        :key="thing.thing_id"
        class="border rounded-2xl px-5 py-4 shrink-0 min-w-[180px] transition-all duration-200 hover:scale-105 cursor-pointer"
        :class="
          selectedThing?.id === thing.thing_id
            ? 'border-[#10B981] bg-[#10B981]/5'
            : 'border-slate-600'
        "
        @click="selectThing(thing)"
      >
        <p class="text-white font-bold uppercase text-sm mb-3 truncate">{{
          thing.thing_name
        }}</p>
        <p class="text-slate-300 text-sm"
          >{{ thing.device_count }}
          {{ thing.device_count === 1 ? 'chip' : 'chips' }}</p
        >
        <p class="text-slate-300 text-sm"
          >consumo {{ formatNumber(thing.total_usage) }}</p
        >
      </div>
    </section>
    <!-- fim dos Cards dos Things(CLIENTES) -->

    <!-- Dados na tabela do Thing(Cliente) selecionado do card acima -->
    <Transition name="panel">
      <section
        v-if="selectedThing || selectedDevice"
        class="bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl overflow-hidden"
      >
        <div
          class="px-5 py-3 border-b border-[#1E293B]/40 flex items-center justify-between"
        >
          <h3 class="text-sm font-bold text-white uppercase tracking-wider">
            Sessões —
            {{
              selectedDevice
                ? selectedDevice.iccid || selectedDevice.iccid || 'Chips'
                : selectedThing.name
            }}
          </h3>
          <span class="text-[11px] text-slate-500"
            >{{ sessionPagination.rowsNumber }} sessões</span
          >
        </div>
        <q-table
          :pagination="sessionPagination"
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
              {{ formatNumber(props.value) }}
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
            Page {{ sessionPagination.page }} de {{ totalPages }}
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
    <!-- Dados na tabela do Thing(Cliente) selecionado do card acima -->
  </main>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { sessionColumns, sessionPagination } from './tableAdmin'
import sessionService from '@/services/session'
import { formatNumber } from '@/utils/format'

const loading = ref(true)
const things = ref([])
const startDate = ref(today())
const endDate = ref(today())
const topDevices = ref([])
const dbDateRange = ref({ min_date: null, max_date: null })
const selectedThing = ref(null)
const selectedDevice = ref(null)
const realusageMin = ref('')
const realusageMax = ref('')

const sessionRows = ref([])
const sessionLoading = ref(false)

const localeBR = {
  days: [
    'Domingo',
    'Segunda-feira',
    'Terça-feira',
    'Quarta-feira',
    'Quinta-feira',
    'Sexta-feira',
    'Sábado'
  ],
  daysShort: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'],
  months: [
    'Janeiro',
    'Fevereiro',
    'Março',
    'Abril',
    'Maio',
    'Junho',
    'Julho',
    'Agosto',
    'Setembro',
    'Outubro',
    'Novembro',
    'Dezembro'
  ],
  monthsShort: [
    'Jan',
    'Fev',
    'Mar',
    'Abr',
    'Mai',
    'Jun',
    'Jul',
    'Ago',
    'Set',
    'Out',
    'Nov',
    'Dez'
  ],
  firstDayOfWeek: 0, // 0 para Domingo, 1 para Segunda-feira
  pluralDay: 'dias'
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const [y, m, d] = dateStr.split('-')
  return `${d}/${m}/${y}`
}

function today() {
  const now = new Date()
  const y = now.getFullYear()
  const m = String(now.getMonth() + 1).padStart(2, '0')
  const d = String(now.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

const totalPages = computed(() =>
  Math.ceil(
    sessionPagination.value.rowsNumber / sessionPagination.value.rowsPerPage
  )
)

const sortedThings = computed(() =>
  [...things.value].sort((a, b) => b.device_count - a.device_count)
)

async function fetchThings(thingId = null) {
  const params = {}
  if (startDate.value) params.start_date = startDate.value
  if (endDate.value) params.end_date = endDate.value
  if (realusageMin.value) params.realusage_min = realusageMin.value
  if (realusageMax.value) params.realusage_max = realusageMax.value
  if (thingId) params.device__thing = thingId
  const [clientes, devices] = await Promise.all([
    sessionService.summaryByThing(params),
    sessionService.topDevices(params)
  ])
  things.value = clientes
  topDevices.value = devices
}

function devicePercent(bytes) {
  if (!topDevices.value.length) return 0
  const max = topDevices.value[0].total_bytes
  return max ? (bytes / max) * 100 : 0
}

async function fetchSessions(props) {
  sessionLoading.value = true
  try {
    const params = {
      page: props.pagination.page,
      page_size: props.pagination.rowsPerPage
    }
    if (selectedDevice.value) {
      params.device = selectedDevice.value.device_id
    } else if (selectedThing.value) {
      params.device__thing = selectedThing.value.id
    }
    if (startDate.value) params.start_date = startDate.value
    if (endDate.value) params.end_date = endDate.value
    if (realusageMin.value) params.realusage_min = realusageMin.value
    if (realusageMax.value) params.realusage_max = realusageMax.value

    const sortBy = props.pagination.sortBy
    const descending = props.pagination.descending
    if (sortBy) {
      params.ordering = descending ? `-${sortBy}` : sortBy
    }

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

function selectThing(thing) {
  if (selectedThing.value?.id === thing.thing_id) {
    selectedThing.value = null
    sessionRows.value = []
    fetchThings()
    return
  }
  selectedThing.value = { id: thing.thing_id, name: thing.thing_name }
  selectedDevice.value = null
  sessionPagination.value.page = 1
  fetchThings(thing.thing_id)
  fetchSessions({
    pagination: { ...sessionPagination.value, page: 1 }
  })
}

function selectDevice(device) {
  if (selectedDevice.value?.device_id === device.device_id) {
    selectedDevice.value = null
    sessionRows.value = []
    fetchThings()
    return
  }
  selectedDevice.value = device
  selectedThing.value = null
  sessionPagination.value.page = 1
  fetchSessions({
    pagination: { ...sessionPagination.value, page: 1 }
  })
}

function clearDates() {
  startDate.value = dbDateRange.value.min_date || today()
  endDate.value = dbDateRange.value.max_date || today()
  realusageMin.value = ''
  realusageMax.value = ''
}

watch([startDate, endDate], () => {
  const thingId = selectedThing.value?.id || null
  fetchThings(thingId)
  if (selectedThing.value || selectedDevice.value) {
    sessionPagination.value.page = 1
    fetchSessions({
      pagination: { ...sessionPagination.value, page: 1 }
    })
  }
})

watch([realusageMin, realusageMax], () => {
  const thingId = selectedThing.value?.id || null
  fetchThings(thingId)
  if (selectedThing.value || selectedDevice.value) {
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
    await fetchThings()
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

<template>
  <aside
    :class="[
      'bg-[#0D1321] border-r border-[#1E293B]/40 flex flex-col shrink-0 transition-all duration-300',
      collapsed ? 'w-16 py-4 px-2' : 'w-64 p-5'
    ]"
  >
    <div :class="collapsed ? 'space-y-3' : 'space-y-8'">
      <div class="flex justify-center">
        <q-img
          src="@/assets/logo_solis.jpg"
          spinner-color="white"
          :style="collapsed ? 'width: 36px' : 'width: 80px'"
          mix-blend-mode="screen"
        />
      </div>

      <nav class="space-y-1">
        <div class="flex items-center">
          <RouterLink
            to="/admin"
            :class="[
              'flex-1 flex items-center rounded-xl font-medium text-xs transition',
              collapsed
                ? 'justify-center px-0 py-2.5'
                : 'space-x-3 px-4 py-2.5',
              isActive('/admin')
                ? 'bg-[#1E293B]/50 text-white'
                : 'text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200'
            ]"
          >
            <svg
              class="w-4 h-4 shrink-0"
              :class="isActive('/admin') ? 'text-[#10B981]' : ''"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
              />
            </svg>
            <span v-if="!collapsed">Dashboard</span>
            <q-tooltip
              v-if="collapsed"
              anchor="center right"
              self="center left"
            >
              Dashboard
            </q-tooltip>
          </RouterLink>
          <button
            class="shrink-0 flex items-center justify-center w-8 h-8 rounded-lg text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200 transition"
            @click="collapsed = !collapsed"
          >
            <svg
              class="w-4 h-4 transition-transform duration-300"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path
                v-if="collapsed"
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M13 5l7 7-7 7M5 5l7 7-7 7"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M11 19l-7-7 7-7m8 14l-7-7 7-7"
              />
            </svg>
            <q-tooltip anchor="center right" self="center left">
              {{ collapsed ? 'Expandir' : 'Recolher' }}
            </q-tooltip>
          </button>
        </div>

        <div class="border-t border-[#1E293B]/40 my-2" />

        <RouterLink
          v-for="item in menuItems"
          :key="item.to"
          :to="item.to"
          :class="[
            'flex items-center rounded-xl font-medium text-xs transition',
            collapsed ? 'justify-center px-0 py-2.5' : 'space-x-3 px-4 py-2.5',
            isActive(item.to)
              ? 'bg-[#1E293B]/50 text-white'
              : 'text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200'
          ]"
        >
          <svg
            class="w-4 h-4 shrink-0"
            :class="isActive(item.to) ? 'text-[#10B981]' : ''"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              :d="item.icon"
            />
          </svg>
          <span v-if="!collapsed">{{ item.label }}</span>
          <q-tooltip v-if="collapsed" anchor="center right" self="center left">
            {{ item.label }}
          </q-tooltip>
        </RouterLink>

        <div class="border-t border-[#1E293B]/40 my-2" />

        <RouterLink
          v-for="item in toolItems"
          :key="item.to"
          :to="item.to"
          :class="[
            'flex items-center rounded-xl font-medium text-xs transition',
            collapsed ? 'justify-center px-0 py-2.5' : 'space-x-3 px-4 py-2.5',
            isActive(item.to)
              ? 'bg-[#1E293B]/50 text-white'
              : 'text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200'
          ]"
        >
          <svg
            class="w-4 h-4 shrink-0"
            :class="isActive(item.to) ? 'text-[#10B981]' : ''"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              :d="item.icon"
            />
          </svg>
          <span v-if="!collapsed">{{ item.label }}</span>
          <q-tooltip v-if="collapsed" anchor="center right" self="center left">
            {{ item.label }}
          </q-tooltip>
        </RouterLink>

        <template v-if="!collapsed">
          <div class="space-y-2">
            <div>
              <label
                class="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1 px-1"
                >De
              </label>
              <div class="q-pa-md" style="max-width: 300px">
                <q-input
                  filled
                  readonly
                  :model-value="formatarDataBR(state.startDate)"
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
                          v-model="state.startDate"
                          mask="YYYY-MM-DD"
                          :locale="localeBR"
                        >
                          <div class="row items-center justify-end">
                            <q-btn
                              v-close-popup
                              label="Close"
                              color="primary"
                              flat
                            />
                          </div>
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
              </div>
            </div>
            <div>
              <label
                class="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1 px-1"
              >
                Até
              </label>
              <div class="q-pa-md" style="max-width: 300px">
                <q-input
                  filled
                  readonly
                  :model-value="formatarDataBR(state.endDate)"
                >
                  <template v-slot:append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy
                        cover
                        transition-show="scale"
                        transition-hide="scale"
                      >
                        <q-date
                          v-model="state.endDate"
                          mask="YYYY-MM-DD"
                          :locale="localeBR"
                        >
                          <div class="row items-center justify-end">
                            <q-btn
                              v-close-popup
                              label="Close"
                              color="primary"
                              flat
                            />
                          </div>
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
              </div>
            </div>
            <q-btn
              flat
              dense
              color="grey"
              label="Limpar"
              icon="clear_all"
              class="shrink-0 whitespace-nowrap"
              @click="clearDates"
            />
            <div class="flex gap-2">
              <q-input
                v-model="state.realusageMin"
                dense
                outlined
                type="number"
                label="Uso mín"
                class="flex-1"
                debounce="300"
              />
              <q-input
                v-model="state.realusageMax"
                dense
                outlined
                type="number"
                label="Uso máx"
                class="flex-1"
                debounce="300"
              />
            </div>
          </div>

          <div class="px-4 py-2">
            <p class="text-[10px] text-slate-500 uppercase tracking-wider"
              >Logado como</p
            >
            <p class="text-xs text-white font-medium truncate">{{
              user?.name || user?.email
            }}</p>
          </div>
        </template>

        <button
          :class="[
            'flex items-center w-full rounded-xl font-medium text-xs transition text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200',
            collapsed ? 'justify-center px-0 py-2.5' : 'space-x-3 px-4 py-2.5'
          ]"
          @click="handleLogout"
        >
          <svg
            class="w-4 h-4 shrink-0"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
            />
          </svg>
          <span v-if="!collapsed">Sair</span>
          <q-tooltip v-if="collapsed" anchor="center right" self="center left">
            Sair
          </q-tooltip>
        </button>
      </nav>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import useAuth from '@/composables/useAuth'
import sessionService from '@/services/session'
import { useDashboardFilter } from '@/composables/useDashboardFilter'

const { state, clearDates: clearFilterDates } = useDashboardFilter()

const loading = ref(true)
const things = ref([])
const topDevices = ref([])
const dbDateRange = ref({ min_date: null, max_date: null })
const selectedThing = ref(null)
const selectedDevice = ref(null)
const collapsed = ref(false)

const route = useRoute()
const router = useRouter()
const { logout, user } = useAuth()

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
  firstDayOfWeek: 0,
  pluralDay: 'dias'
}

const formatarDataBR = val => {
  if (!val) return ''
  const [y, m, d] = val.split('-')
  return `${d}/${m}/${y}`
}

function today() {
  const now = new Date()
  const y = now.getFullYear()
  const m = String(now.getMonth() + 1).padStart(2, '0')
  const d = String(now.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

function clearDates() {
  state.startDate = dbDateRange.value.min_date || today()
  state.endDate = dbDateRange.value.max_date || today()
  state.realusageMin = ''
  state.realusageMax = ''
}

function handleLogout() {
  logout()
  router.push('/login')
}

const menuItems = [
  {
    label: 'Clientes',
    to: '/admin/thing',
    icon: 'M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z'
  },
  {
    label: 'Usuários',
    to: '/admin/profile',
    icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z'
  },
  {
    label: 'Sessões',
    to: '/admin/session',
    icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z'
  }
]

const toolItems = [
  {
    label: 'Importar CDR',
    to: '/admin/xlsx',
    icon: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12'
  }
]

function isActive(to) {
  return route.path === to
}

onMounted(async () => {
  try {
    const range = await sessionService.dateRange()
    dbDateRange.value = range
    if (range.min_date) state.startDate = range.min_date
    if (range.max_date) state.endDate = range.max_date
  } finally {
    loading.value = false
  }
})
</script>

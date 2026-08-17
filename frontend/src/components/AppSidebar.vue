<template>
  <aside
    :class="[
      'bg-[#0D1321] border-r border-[#1E293B]/40 flex flex-col justify-between shrink-0 transition-all duration-300',
      collapsed ? 'w-16 py-4 px-2' : 'w-64 p-5'
    ]"
  >
    <div :class="collapsed ? 'space-y-3' : 'space-y-6'">
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
            to="/"
            :class="[
              'flex-1 flex items-center rounded-xl font-medium text-xs transition',
              collapsed
                ? 'justify-center px-0 py-2.5'
                : 'space-x-3 px-4 py-2.5',
              isActive('/')
                ? 'bg-[#1E293B]/50 text-white'
                : 'text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200'
            ]"
          >
            <svg
              class="w-4 h-4 shrink-0"
              :class="isActive('/') ? 'text-[#10B981]' : ''"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M4 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2v-4zM14 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4z"
              />
            </svg>
            <span v-if="!collapsed">Painel</span>
            <q-tooltip
              v-if="collapsed"
              anchor="center right"
              self="center left"
            >
              Painel
            </q-tooltip>
          </RouterLink>
          <button
            class="shrink-0 flex items-center justify-center w-8 h-8 rounded-lg text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200 transition"
            @click="collapsed = !collapsed"
          >
            <span class="text-xs font-bold">{{ collapsed ? '>>' : '<<' }}</span>
            <q-tooltip anchor="center right" self="center left">
              {{ collapsed ? 'Expandir' : 'Recolher' }}
            </q-tooltip>
          </button>
        </div>

        <template v-if="!collapsed">
          <div class="border-t border-[#1E293B]/40 my-2" />

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
            <button
              v-if="state.startDate || state.endDate"
              class="text-[10px] text-slate-500 hover:text-slate-300 transition px-1"
              @click="clearDates"
              >Limpar datas</button
            >
          </div>
        </template>
      </nav>
    </div>

    <div class="space-y-1">
      <div v-if="!collapsed" class="px-4 py-2">
        <p class="text-[10px] text-slate-500 uppercase tracking-wider"
          >Logado como</p
        >
        <p class="text-xs text-white font-medium truncate">{{
          user?.name || user?.email
        }}</p>
      </div>

      <RouterLink
        v-if="canAccessAdmin"
        to="/admin"
        :class="[
          'flex items-center rounded-xl font-medium text-xs transition',
          collapsed ? 'justify-center px-0 py-2.5' : 'space-x-3 px-4 py-2.5',
          'text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200'
        ]"
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
            d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
          />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
          />
        </svg>
        <span v-if="!collapsed">Admin</span>
        <q-tooltip v-if="collapsed" anchor="center right" self="center left">
          Admin
        </q-tooltip>
      </RouterLink>

      <button
        :class="[
          'flex items-center w-full rounded-xl font-medium text-xs transition',
          collapsed ? 'justify-center px-0 py-2.5' : 'space-x-3 px-4 py-2.5',
          'text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200'
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
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import useAuth from '@/composables/useAuth'
import { useDashboardFilter } from '@/composables/useDashboardFilter'

const route = useRoute()
const router = useRouter()
const { logout, canAccessAdmin, user } = useAuth()
const { state, clearDates } = useDashboardFilter()
const collapsed = ref(false)

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

defineProps({
  alertCount: {
    type: Number,
    default: 0
  }
})

const formatarDataBR = val => {
  if (!val) return ''
  const [y, m, d] = val.split('-')
  return `${d}/${m}/${y}`
}

function handleLogout() {
  logout()
  router.push('/login')
}

function isActive(to) {
  return route.path === to
}
</script>

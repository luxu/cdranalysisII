<template>
  <aside
    class="w-64 bg-[#0D1321] border-r border-[#1E293B]/40 flex flex-col justify-between p-5 shrink-0"
  >
    <div class="space-y-6">
      <div class="flex items-center space-x-3 px-2">
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
              d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m12.728 0l-.707-.707M6.343 6.343l-.707-.707M14 12a2 2 0 11-4 0 2 2 0 014 0z"
            />
          </svg>
        </div>
        <div>
          <h2 class="text-sm font-bold text-white tracking-wide">SOLIS</h2>
          <p class="text-[10px] text-slate-500 font-medium"
            >Monitoramento Inteligente</p
          >
        </div>
      </div>

      <nav class="space-y-1">
        <RouterLink
          v-for="item in mainLinks"
          :key="item.to"
          :to="item.to"
          class="flex items-center space-x-3 px-4 py-2.5 rounded-xl font-medium text-xs transition"
          :class="
            isActive(item.to)
              ? 'bg-[#1E293B]/50 text-white'
              : 'text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200'
          "
        >
          <svg
            class="w-4 h-4"
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
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>

      <div class="border-t border-[#1E293B]/40 pt-4 space-y-3">
        <div class="flex items-center space-x-2 px-2">
          <svg
            class="w-3.5 h-3.5 text-slate-500 shrink-0"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"
            />
          </svg>
          <span
            class="text-[10px] font-semibold text-slate-500 uppercase tracking-wider"
            >Filtros</span
          >
        </div>

        <div class="relative">
          <svg
            class="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-500"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
          <input
            v-model="state.search"
            type="text"
            placeholder="Buscar dispositivo..."
            class="w-full bg-[#090D16] border border-[#1E293B]/40 text-xs text-slate-300 placeholder-slate-600 rounded-xl pl-9 pr-3 py-2.5 focus:outline-none focus:border-[#10B981]/50 transition"
          />
        </div>

        <div class="flex items-center space-x-3 px-1">
          <label class="flex items-center space-x-2 cursor-pointer">
            <input
              type="checkbox"
              v-model="state.statusAtivo"
              class="w-3.5 h-3.5 rounded border-slate-600 bg-[#090D16] text-[#10B981] focus:ring-[#10B981]/30 focus:ring-offset-0 cursor-pointer"
            />
            <span class="text-[11px] text-slate-400">Ativo</span>
          </label>
          <label class="flex items-center space-x-2 cursor-pointer">
            <input
              type="checkbox"
              v-model="state.statusInativo"
              class="w-3.5 h-3.5 rounded border-slate-600 bg-[#090D16] text-rose-500 focus:ring-rose-500/30 focus:ring-offset-0 cursor-pointer"
            />
            <span class="text-[11px] text-slate-400">Inativo</span>
          </label>
        </div>

        <div class="space-y-2">
          <div>
            <label
              class="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1 px-1"
              >De</label
            >
            <input
              type="date"
              v-model="state.startDate"
              class="w-full bg-[#090D16] border border-[#1E293B]/40 text-xs text-slate-300 rounded-xl px-3 py-2 focus:outline-none focus:border-[#10B981]/50 transition [color-scheme:dark]"
            />
          </div>
          <div>
            <label
              class="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1 px-1"
              >Até</label
            >
            <input
              type="date"
              v-model="state.endDate"
              class="w-full bg-[#090D16] border border-[#1E293B]/40 text-xs text-slate-300 rounded-xl px-3 py-2 focus:outline-none focus:border-[#10B981]/50 transition [color-scheme:dark]"
            />
          </div>
          <button
            v-if="state.startDate || state.endDate"
            class="text-[10px] text-slate-500 hover:text-slate-300 transition px-1"
            @click="clearDates"
            >Limpar datas</button
          >
        </div>
      </div>
    </div>

    <div class="space-y-1">
      <RouterLink
        v-if="canAccessAdmin"
        to="/admin"
        class="flex items-center space-x-3 px-4 py-2.5 rounded-xl text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200 font-medium text-xs transition"
      >
        <svg
          class="w-4 h-4"
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
        <span>Admin</span>
      </RouterLink>

      <button
        class="flex items-center space-x-3 w-full px-4 py-2.5 rounded-xl text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200 font-medium text-xs transition"
        @click="handleLogout"
      >
        <svg
          class="w-4 h-4"
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
        <span>Sair</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import useAuth from '@/composables/useAuth'
import { useDashboardFilter } from '@/composables/useDashboardFilter'

defineProps({
  alertCount: {
    type: Number,
    default: 0
  }
})

const route = useRoute()
const router = useRouter()
const { logout, canAccessAdmin } = useAuth()
const { state, clearDates } = useDashboardFilter()

function handleLogout() {
  logout()
  router.push('/login')
}

const mainLinks = [
  {
    label: 'Painel',
    to: '/',
    icon: 'M4 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2v-4zM14 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4z'
  }
]

function isActive(to) {
  return route.path === to
}
</script>

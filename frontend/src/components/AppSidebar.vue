<template>
  <aside
    class="w-64 bg-[#0D1321] border-r border-[#1E293B]/40 flex flex-col justify-between p-5 shrink-0"
  >
    <div class="space-y-8">
      <!-- Logo / Nome do Sistema -->
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
          <h2 class="text-sm font-bold text-white tracking-wide">AgroIoT</h2>
          <p class="text-[10px] text-slate-500 font-medium"
            >Monitoramento Inteligente</p
          >
        </div>
      </div>

      <!-- Links de Navegação Principal -->
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
    </div>

    <!-- Links Configurações / Alertas -->
    <div class="space-y-1">
      <RouterLink
        to="/alertas"
        class="flex items-center justify-between px-4 py-2.5 rounded-xl text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200 font-medium text-xs transition"
      >
        <div class="flex items-center space-x-3">
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
              d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.641C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
            />
          </svg>
          <span>Alertas</span>
        </div>
        <span
          v-if="alertCount > 0"
          class="bg-rose-600 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-md"
        >
          {{ alertCount }}
        </span>
      </RouterLink>

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

defineProps({
  alertCount: {
    type: Number,
    default: 3
  }
})

const route = useRoute()
const router = useRouter()
const { logout, canAccessAdmin } = useAuth()

function handleLogout() {
  logout()
  router.push('/login')
}

const mainLinks = [
  {
    label: 'Painel',
    to: '/',
    icon: 'M4 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2v-4zM14 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4z'
  },
  {
    label: 'Temperatura',
    to: '/temperatura',
    icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2'
  },
  {
    label: 'Umidade',
    to: '/umidade',
    icon: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z'
  },
  {
    label: 'Pluviometria',
    to: '/pluviometria',
    icon: 'M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z'
  },
  {
    label: 'Reservatórios',
    to: '/reservatorios',
    icon: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z'
  },
  {
    label: 'Equipamentos',
    to: '/equipamentos',
    icon: 'M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 5h10a2 2 0 012 2v10a2 2 0 01-2 2H7a2 2 0 01-2-2V7a2 2 0 012-2z'
  }
]

function isActive(to) {
  return route.path === to
}
</script>

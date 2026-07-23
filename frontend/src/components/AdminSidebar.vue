<template>
  <aside
    class="w-64 bg-[#0D1321] border-r border-[#1E293B]/40 flex flex-col justify-between p-5 shrink-0"
  >
    <div class="space-y-8">
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
              d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
            />
          </svg>
        </div>
        <div>
          <h2 class="text-sm font-bold text-white tracking-wide">SOLIS</h2>
          <p class="text-[10px] text-slate-500 font-medium">Administração</p>
        </div>
      </div>

      <nav class="space-y-1">
        <RouterLink
          v-for="item in menuItems"
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

    <div class="space-y-1">
      <RouterLink
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
            d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
          />
        </svg>
        <span>Dashboard Admin</span>
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

const route = useRoute()
const router = useRouter()
const { logout } = useAuth()

function handleLogout() {
  logout()
  router.push('/login')
}

const menuItems = [
  {
    label: 'Things(Clientes)',
    to: '/admin/thing',
    icon: 'M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z'
  },
  {
    label: 'Profiles',
    to: '/admin/profile',
    icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z'
  },
  {
    label: 'Importar CDR',
    to: '/admin/xlsx',
    icon: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12'
  },
  {
    label: 'Sessions',
    to: '/admin/session',
    icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z'
  }
]

function isActive(to) {
  return route.path === to
}
</script>

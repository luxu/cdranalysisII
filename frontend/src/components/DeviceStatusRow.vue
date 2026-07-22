<template>
  <div
    class="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-2xl bg-[#090D16]/40 border border-[#1E293B]/20 gap-4"
  >
    <div class="flex items-center space-x-4">
      <div
        class="p-2.5 rounded-xl border"
        :style="{
          backgroundColor: `${statusStyle.color}1A`,
          borderColor: `${statusStyle.color}33`,
          color: statusStyle.color
        }"
      >
        <svg
          class="w-4 h-4"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" :d="icon" />
        </svg>
      </div>
      <div>
        <h4 class="text-sm font-semibold text-white">{{ name }}</h4>
        <p class="text-[11px] text-slate-500 font-medium">{{ location }}</p>
      </div>
    </div>

    <div class="flex items-center space-x-6 text-xs font-medium text-slate-400">
      <span
        class="px-2.5 py-1 rounded-lg border text-[10px] font-bold"
        :style="{
          backgroundColor: `${statusStyle.color}1A`,
          borderColor: `${statusStyle.color}33`,
          color: statusStyle.color
        }"
      >
        {{ status }}
      </span>
      <span
        class="flex items-center gap-1 font-mono text-[11px]"
        :class="{ 'text-rose-400/80': status === 'Offline' }"
      >
        🪫 {{ battery }}%
      </span>
      <span
        class="flex items-center gap-1 font-mono text-[11px]"
        :class="{ 'text-rose-400/80': status === 'Offline' }"
      >
        📶 {{ signal }}%
      </span>
      <span class="text-slate-500 font-normal text-[11px]">{{
        updatedAt
      }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  icon: { type: String, required: true },
  name: { type: String, required: true },
  location: { type: String, required: true },
  status: { type: String, required: true }, // 'Online' | 'Offline' | 'Manutenção'
  battery: { type: Number, required: true },
  signal: { type: Number, required: true },
  updatedAt: { type: String, required: true }
})

const STATUS_COLORS = {
  Online: '#10B981',
  Offline: '#F43F5E',
  Manutenção: '#F59E0B'
}

const statusStyle = computed(() => ({
  color: STATUS_COLORS[props.status] || '#10B981'
}))
</script>

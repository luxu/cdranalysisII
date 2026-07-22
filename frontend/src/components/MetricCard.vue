<template>
  <div
    class="bg-[#0D1321] border border-[#1E293B]/50 rounded-2xl p-5 flex flex-col justify-between space-y-4"
  >
    <div class="flex items-center justify-between">
      <div
        class="p-2 rounded-xl border"
        :style="{
          backgroundColor: `${color}1A`,
          borderColor: `${color}33`,
          color: color
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
      <span
        class="text-[10px] font-bold flex items-center gap-1"
        :style="{ color: statusColor }"
      >
        <span
          class="w-1 h-1 rounded-full"
          :class="{ 'animate-pulse': status === 'Atenção' }"
          :style="{ backgroundColor: statusColor }"
        />
        {{ status }}
      </span>
    </div>

    <div>
      <span class="text-xs font-medium text-slate-400">{{ label }}</span>
      <h3 class="text-3xl font-bold text-white mt-1">
        {{ value
        }}<span class="text-sm font-medium text-slate-400"> {{ unit }}</span>
      </h3>
    </div>

    <div class="space-y-1">
      <div class="w-full bg-slate-800 h-1 rounded-full overflow-hidden">
        <div
          class="h-full"
          :style="{ width: `${percentage}%`, backgroundColor: barColor }"
        />
      </div>
      <div class="flex justify-between text-[10px] font-mono text-slate-500">
        <span>{{ min }}</span>
        <span>{{ max }}</span>
      </div>
    </div>

    <div
      class="flex justify-between items-center pt-1 border-t border-slate-800 text-[10px] font-medium text-slate-500"
    >
      <span class="flex items-center gap-1">
        <span class="w-1 h-1 rounded-full bg-slate-400" /> {{ protocol }}
      </span>
      <span>{{ updatedAt }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  icon: { type: String, required: true },
  color: { type: String, required: true },
  label: { type: String, required: true },
  value: { type: [String, Number], required: true },
  unit: { type: String, default: '' },
  percentage: { type: Number, required: true },
  min: { type: String, required: true },
  max: { type: String, required: true },
  protocol: { type: String, required: true },
  updatedAt: { type: String, required: true },
  status: { type: String, default: 'Normal' }
})

const statusColor = computed(() =>
  props.status === 'Atenção' ? '#F59E0B' : '#10B981'
)
const barColor = computed(() =>
  props.percentage < 10
    ? '#475569'
    : props.status === 'Atenção'
      ? '#F59E0B'
      : '#10B981'
)
</script>

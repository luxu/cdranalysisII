<template>
  <main class="flex-1 p-8 space-y-6 overflow-y-auto">
    <section
      class="bg-[#0D1321] border border-[#1E293B]/40 rounded-3xl p-6 shadow-sm space-y-4"
    >
      <!-- Cabeçalho -->
      <div
        class="flex items-center justify-between pb-2 border-b border-[#1E293B]/30"
      >
        <h3 class="text-base font-semibold text-white tracking-tight"
          >Equipamentos IoT</h3
        >
        <div class="flex items-center space-x-4 text-xs font-medium">
          <span class="flex items-center gap-1.5 text-slate-400">
            <span class="w-1.5 h-1.5 rounded-full bg-[#10B981]" />
            {{ onlineCount }} online
          </span>
          <span class="flex items-center gap-1.5 text-slate-400">
            <span class="w-1.5 h-1.5 rounded-full bg-rose-500" />
            {{ offlineCount }} offline
          </span>
        </div>
      </div>

      <!-- Lista de Dispositivos -->
      <div class="space-y-2">
        <DeviceStatusRow
          v-for="device in devices"
          :key="device.name"
          v-bind="device"
        />
      </div>
    </section>
    <!-- Cards Inferiores Institucionais -->
    <section class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <InstitutionalCard
        v-for="card in institutionalCards"
        :key="card.title"
        v-bind="card"
      />
    </section>
  </main>
</template>

<script setup>
import { computed } from 'vue'
import DeviceStatusRow from '@/components/DeviceStatusRow.vue'
import InstitutionalCard from '@/components/InstitutionalCard.vue'

const ICONS = {
  cloud:
    'M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z',
  droplet:
    'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z',
  chip: 'M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 5h10a2 2 0 012 2v10a2 2 0 01-2 2H7a2 2 0 01-2-2V7a2 2 0 012-2z',
  offline:
    'M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636',
  camera:
    'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z'
}

const devices = [
  {
    icon: ICONS.cloud,
    name: 'Estação Meteorológica A1',
    location: 'Setor Norte - Talhão 3',
    status: 'Online',
    battery: 92,
    signal: 95,
    updatedAt: '30s atrás'
  },
  {
    icon: ICONS.droplet,
    name: 'Sensor de Solo B2',
    location: 'Setor Leste - Talhão 7',
    status: 'Online',
    battery: 68,
    signal: 78,
    updatedAt: '2min atrás'
  },
  {
    icon: ICONS.droplet,
    name: 'Controlador de Irrigação C1',
    location: 'Setor Sul - Pivô Central',
    status: 'Online',
    battery: 100,
    signal: 88,
    updatedAt: '15s atrás'
  },
  {
    icon: ICONS.chip,
    name: 'Gateway LoRa D1',
    location: 'Torre Central',
    status: 'Online',
    battery: 100,
    signal: 99,
    updatedAt: '5s atrás'
  },
  {
    icon: ICONS.offline,
    name: 'Sensor Pluviométrico E1',
    location: 'Setor Oeste - Talhão 12',
    status: 'Offline',
    battery: 12,
    signal: 0,
    updatedAt: '3h atrás'
  },
  {
    icon: ICONS.camera,
    name: 'Câmera de Monitoramento F1',
    location: 'Entrada Principal',
    status: 'Manutenção',
    battery: 100,
    signal: 45,
    updatedAt: '1h atrás'
  }
]

const onlineCount = computed(
  () => devices.filter(d => d.status === 'Online').length
)
const offlineCount = computed(
  () => devices.filter(d => d.status === 'Offline').length
)

const institutionalCards = [
  {
    image:
      'https://images.unsplash.com/photo-1560493458-3e5b17a6212e?auto=format&fit=crop&q=80&w=600',
    title: 'Sensores no Campo',
    description: 'Comunicação direta via redes estáveis LoRa e MQTT'
  },
  {
    image:
      'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&q=80&w=600',
    title: 'Estufas Automatizadas',
    description: 'Irrigação e controle microclimático inteligente via Zigbee'
  }
]
</script>

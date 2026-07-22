<template>
  <main class="flex-1 p-8 space-y-6 overflow-y-auto">
    <!-- Topo: Nome da Fazenda e Conectividade -->
    <section
      class="flex flex-col md:flex-row md:items-center md:justify-between gap-4"
    >
      <div>
        <div class="flex items-center space-x-3">
          <h1 class="text-2xl font-bold text-white tracking-tight">{{
            farm.name
          }}</h1>
          <span
            class="bg-[#10B981]/10 text-[#10B981] text-[10px] font-bold px-2 py-0.5 rounded-full border border-[#10B981]/20 flex items-center gap-1"
          >
            <span class="w-1.5 h-1.5 rounded-full bg-[#10B981]" />
            {{ farm.status }}
          </span>
        </div>
        <div
          class="flex items-center space-x-4 text-xs text-slate-400 mt-1 font-medium"
        >
          <span class="flex items-center gap-1">📍 Ribeirão Preto, SP</span>
          <span class="flex items-center gap-1">📐 {{ farm.area }}</span>
        </div>
      </div>

      <!-- Contador de Sensores Conectados -->
      <div
        class="flex items-center space-x-4 bg-[#0D1321] border border-[#1E293B]/40 px-5 py-3 rounded-2xl"
      >
        <div class="text-right">
          <span
            class="text-[10px] font-bold text-slate-500 uppercase block tracking-wider"
            >Sensores Conectados</span
          >
          <span class="text-lg font-bold text-white">
            {{ sensors.connected
            }}<span class="text-slate-500 text-sm">/{{ sensors.total }}</span>
            <span class="text-xs text-slate-400 font-normal">
              ({{ sensors.percentage }}%)</span
            >
          </span>
        </div>
        <div class="relative w-10 h-10 flex items-center justify-center">
          <svg class="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
            <path
              class="text-slate-800"
              stroke-width="3.5"
              stroke="currentColor"
              fill="none"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
            />
            <path
              class="text-[#10B981]"
              :stroke-dasharray="`${sensors.percentage}, 100`"
              stroke-width="3.5"
              stroke-linecap="round"
              stroke="currentColor"
              fill="none"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
            />
          </svg>
          <span class="absolute text-[9px] font-bold text-white"
            >{{ sensors.percentage }}%</span
          >
        </div>
      </div>
    </section>

    <!-- Banner Hero -->
    <section
      class="relative h-60 w-full overflow-hidden rounded-3xl bg-slate-900 border border-[#1E293B]/30 shadow-sm flex items-end p-6"
    >
      <img
        src="https://images.unsplash.com/photo-1592982537447-744077110b84?auto=format&fit=crop&q=80&w=1200"
        alt="Vista Aérea Lavoura"
        class="absolute inset-0 w-full h-full object-cover opacity-40 brightness-75"
      />
      <div
        class="absolute inset-0 bg-gradient-to-t from-[#090D16] via-transparent to-transparent"
      />

      <div
        class="relative flex items-center space-x-3 bg-[#090D16]/80 backdrop-blur-md px-4 py-2.5 rounded-2xl border border-[#1E293B]/40 max-w-md"
      >
        <div class="text-[#10B981]">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.77.946.669.752 1.109 1.706 1.205 2.76.023.25.034.503.034.757a7.969 7.969 0 01-.416 2.547h.81a1 1 0 00.993-.883l.5-4.375a1 1 0 00-.535-.98l-.371-.186zm-1.876.549A5.968 5.968 0 009.023 2c-1.157 0-2.23.328-3.14.895l-.37.185a1 1 0 00-.536.98l.5 4.375a1 1 0 00.993.883h.81A7.97 7.97 0 017 6.77c0-.254.01-.506.034-.756.096-1.054.536-2.008 1.205-2.76a1 1 0 00-.77-.946zM2 13a1 1 0 011-1h14a1 1 0 110 2H3a1 1 0 01-1-1zm1 3a1 1 0 100 2h14a1 1 0 100-2H3z"
              clip-rule="evenodd"
            />
          </svg>
        </div>
        <div>
          <h4 class="text-xs font-bold text-white"
            >Monitoramento em Tempo Real</h4
          >
          <p class="text-[10px] text-slate-400 mt-0.5"
            >Dados coletados e atualizados via rede IoT</p
          >
        </div>
      </div>
    </section>

    <!-- Grid de Cards -->
    <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <MetricCard v-for="card in metricCards" :key="card.label" v-bind="card" />
    </section>

    <!-- Gráficos -->
    <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div
        class="bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-5 shadow-sm"
      >
        <div class="flex items-center justify-between mb-4">
          <span class="text-xs font-semibold text-white">Temperatura</span>
          <span class="text-[11px] text-slate-400 font-medium">
            Últimas 24h <strong class="text-white ml-1">28.5°C</strong>
          </span>
        </div>
        <apexchart
          type="line"
          height="220"
          :options="temperatureChart.options"
          :series="temperatureChart.series"
        />
      </div>

      <div
        class="bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-5 shadow-sm"
      >
        <div class="flex items-center justify-between mb-4">
          <span class="text-xs font-semibold text-white">Umidade do Solo</span>
          <span class="text-[11px] text-slate-400 font-medium">
            Últimas 24h <strong class="text-white ml-1">62.3%</strong>
          </span>
        </div>
        <apexchart
          type="line"
          height="220"
          :options="humidityChart.options"
          :series="humidityChart.series"
        />
      </div>
    </section>

    <!-- Bloco de Equipamentos IoT -->
    <section
      class="bg-[#0D1321] border border-[#1E293B]/40 rounded-3xl p-6 shadow-sm space-y-4"
    >
      <div
        class="flex items-center justify-between pb-2 border-b border-[#1E293B]/30"
      >
        <h3 class="text-base font-semibold text-white tracking-tight"
          >Equipamentos IoT</h3
        >
        <div class="flex items-center space-x-4 text-xs font-medium">
          <span class="flex items-center gap-1.5 text-slate-400">
            <span class="w-1.5 h-1.5 rounded-full bg-[#10B981]" /> 4 online
          </span>
          <span class="flex items-center gap-1.5 text-slate-400">
            <span class="w-1.5 h-1.5 rounded-full bg-rose-500" /> 1 offline
          </span>
        </div>
      </div>

      <div class="space-y-2">
        <DeviceStatusRow
          v-for="device in devices"
          :key="device.name"
          v-bind="device"
        />
      </div>
    </section>

    <!-- Cards Institucionais -->
    <section class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <InstitutionalCard
        image="https://images.unsplash.com/photo-1560493458-3e5b17a6212e?auto=format&fit=crop&q=80&w=600"
        title="Sensores no Campo"
        description="Comunicação direta via redes estáveis LoRa e MQTT"
      />
      <InstitutionalCard
        image="https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&q=80&w=600"
        title="Estufas Automatizadas"
        description="Irrigação e controle microclimático inteligente via Zigbee"
      />
    </section>
  </main>
</template>

<script setup>
import { reactive } from 'vue'
import MetricCard from '@/components/MetricCard.vue'
import DeviceStatusRow from '@/components/DeviceStatusRow.vue'
import InstitutionalCard from '@/components/InstitutionalCard.vue'

const farm = reactive({
  name: 'Fazenda Santa Clara',
  status: 'Ativa',
  location: 'Curitiba, PR',
  area: '1.250 hectares'
})

const sensors = reactive({
  connected: 22,
  total: 24,
  percentage: 92
})

const metricCards = [
  {
    icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2',
    color: '#F97316',
    label: 'Temperatura Ambiente',
    value: '28.5',
    unit: '°C',
    percentage: 52,
    min: '18°C',
    max: '38°C',
    protocol: 'MQTT',
    updatedAt: '2 min atrás',
    status: 'Normal'
  },
  {
    icon: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z',
    color: '#3B82F6',
    label: 'Umidade do Solo',
    value: '62.3',
    unit: '%',
    percentage: 65,
    min: '30%',
    max: '90%',
    protocol: 'LoRa',
    updatedAt: '5 min atrás',
    status: 'Normal'
  },
  {
    icon: 'M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z',
    color: '#06B6D4',
    label: 'Pluviometria',
    value: '2.4',
    unit: 'mm',
    percentage: 8,
    min: '0mm',
    max: '50mm',
    protocol: 'LoRa',
    updatedAt: '10 min atrás',
    status: 'Normal'
  },
  {
    icon: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z',
    color: '#F59E0B',
    label: 'Nível do Reservatório',
    value: '74.8',
    unit: '%',
    percentage: 74.8,
    min: '20%',
    max: '100%',
    protocol: 'Zigbee',
    updatedAt: '1 min atrás',
    status: 'Atenção'
  }
]

const devices = [
  {
    icon: 'M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z',
    name: 'Estação Meteorológica A1',
    location: 'Setor Norte - Talhão 3',
    status: 'Online',
    battery: 92,
    signal: 95,
    updatedAt: '30s atrás'
  },
  {
    icon: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z',
    name: 'Sensor de Solo B2',
    location: 'Setor Leste - Talhão 7',
    status: 'Online',
    battery: 68,
    signal: 78,
    updatedAt: '2min atrás'
  },
  {
    icon: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z',
    name: 'Controlador de Irrigação C1',
    location: 'Setor Sul - Pivô Central',
    status: 'Online',
    battery: 100,
    signal: 88,
    updatedAt: '15s atrás'
  },
  {
    icon: 'M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 5h10a2 2 0 012 2v10a2 2 0 01-2 2H7a2 2 0 01-2-2V7a2 2 0 012-2z',
    name: 'Gateway LoRa D1',
    location: 'Torre Central',
    status: 'Online',
    battery: 100,
    signal: 99,
    updatedAt: '5s atrás'
  },
  {
    icon: 'M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636',
    name: 'Sensor Pluviométrico E1',
    location: 'Setor Oeste - Talhão 12',
    status: 'Offline',
    battery: 12,
    signal: 0,
    updatedAt: '3h atrás'
  },
  {
    icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z',
    name: 'Câmera de Monitoramento F1',
    location: 'Entrada Principal',
    status: 'Manutenção',
    battery: 100,
    signal: 45,
    updatedAt: '1h atrás'
  }
]

// Opções base para gráficos no tema dark (reaproveite entre os dois)
function buildChartOptions(color) {
  return {
    chart: {
      toolbar: { show: false },
      background: 'transparent',
      zoom: { enabled: false }
    },
    theme: { mode: 'dark' },
    grid: { borderColor: '#1E293B', strokeDashArray: 4 },
    stroke: { curve: 'smooth', width: 2 },
    colors: [color],
    dataLabels: { enabled: false },
    xaxis: {
      categories: ['00h', '04h', '08h', '12h', '16h', '20h', '23h'],
      labels: { style: { colors: '#64748B', fontSize: '10px' } },
      axisBorder: { show: false },
      axisTicks: { show: false }
    },
    yaxis: {
      labels: { style: { colors: '#64748B', fontSize: '10px' } }
    },
    tooltip: { theme: 'dark' },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.35,
        opacityTo: 0.05,
        stops: [0, 90, 100]
      }
    }
  }
}

const temperatureChart = reactive({
  options: buildChartOptions('#F97316'),
  series: [{ name: 'Temperatura', data: [22, 21, 24, 30, 32, 28, 28.5] }]
})

const humidityChart = reactive({
  options: buildChartOptions('#3B82F6'),
  series: [{ name: 'Umidade', data: [58, 60, 55, 50, 57, 61, 62.3] }]
})
</script>

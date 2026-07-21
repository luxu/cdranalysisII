<template>
  <q-page class="flex flex-center">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>AgroIoT - Painel Integrado</title>      
  </head>
    <!-- 1. SIDEBAR LATERAL ESQUERDA -->
    <aside class="w-64 bg-[#0D1321] border-r border-[#1E293B]/40 flex flex-col justify-between p-5 shrink-0">
        <div class="space-y-8">
            <!-- Logo / Nome do Sistema -->
            <div class="flex items-center space-x-3 px-2">
                <div class="bg-[#10B981]/10 text-[#10B981] p-2 rounded-xl border border-[#10B981]/20">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m12.728 0l-.707-.707M6.343 6.343l-.707-.707M14 12a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
                </div>
                <div>
                    <h2 class="text-sm font-bold text-white tracking-wide">AgroIoT</h2>
                    <p class="text-[10px] text-slate-500 font-medium">Monitoramento Inteligente</p>
                </div>
            </div>

            <!-- Links de Navegação Principal -->
            <nav class="space-y-1">
                <a href="#" class="flex items-center space-x-3 px-4 py-2.5 rounded-xl bg-[#1E293B]/50 text-white font-medium text-xs transition">
                    <svg class="w-4 h-4 text-[#10B981]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2v-4zM14 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4z"></path></svg>
                    <span>Painel</span>
                </a>
                <a href="#" class="flex items-center space-x-3 px-4 py-2.5 rounded-xl text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200 font-medium text-xs transition">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2"></path></svg>
                    <span>Temperatura</span>
                </a>
                <a href="#" class="flex items-center space-x-3 px-4 py-2.5 rounded-xl text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200 font-medium text-xs transition">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
                    <span>Umidade</span>
                </a>
                <a href="#" class="flex items-center space-x-3 px-4 py-2.5 rounded-xl text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200 font-medium text-xs transition">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path></svg>
                    <span>Pluviometria</span>
                </a>
                <a href="#" class="flex items-center space-x-3 px-4 py-2.5 rounded-xl text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200 font-medium text-xs transition">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
                    <span>Reservatórios</span>
                </a>
                <a href="#" class="flex items-center space-x-3 px-4 py-2.5 rounded-xl text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200 font-medium text-xs transition">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 5h10a2 2 0 012 2v10a2 2 0 01-2 2H7a2 2 0 01-2-2V7a2 2 0 012-2z"></path></svg>
                    <span>Equipamentos</span>
                </a>
            </nav>
        </div>

        <!-- Links Configurações / Alertas -->
        <div class="space-y-1">
            <a href="#" class="flex items-center justify-between px-4 py-2.5 rounded-xl text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200 font-medium text-xs transition">
                <div class="flex items-center space-x-3">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.641C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
                    <span>Alertas</span>
                </div>
                <span class="bg-rose-600 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-md">3</span>
            </a>
            <a href="#" class="flex items-center space-x-3 px-4 py-2.5 rounded-xl text-slate-400 hover:bg-[#1E293B]/20 hover:text-slate-200 font-medium text-xs transition">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                <span>Configurações</span>
            </a>
        </div>
    </aside>

    <!-- 2. CONTEÚDO PRINCIPAL DIREITO -->
    <main class="flex-1 p-8 space-y-6 overflow-y-auto">
        
        <!-- Topo da Página (Nome da Fazenda e Métricas de Conectividade) -->
        <section class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
                <div class="flex items-center space-x-3">
                    <h1 class="text-2xl font-bold text-white tracking-tight">Fazenda Santa Clara</h1>
                    <span class="bg-[#10B981]/10 text-[#10B981] text-[10px] font-bold px-2 py-0.5 rounded-full border border-[#10B981]/20 flex items-center gap-1">
                        <span class="w-1.5 h-1.5 rounded-full bg-[#10B981]"></span> Ativa
                    </span>
                </div>
                <div class="flex items-center space-x-4 text-xs text-slate-400 mt-1 font-medium">
                    <span class="flex items-center gap-1">📍 Ribeirão Preto, SP</span>
                    <span class="flex items-center gap-1">📐 1.250 hectares</span>
                </div>
            </div>

            <!-- Contador Redondo de Dispositivos Conectados -->
            <div class="flex items-center space-x-4 bg-[#0D1321] border border-[#1E293B]/40 px-5 py-3 rounded-2xl">
                <div class="text-right">
                    <span class="text-[10px] font-bold text-slate-500 uppercase block tracking-wider">Sensores Conectados</span>
                    <span class="text-lg font-bold text-white">22<span class="text-slate-500 text-sm">/24</span> <span class="text-xs text-slate-400 font-normal">(92%)</span></span>
                </div>
                <!-- Mini Gráfico de Rosca Pure CSS/SVG -->
                <div class="relative w-10 h-10 flex items-center justify-center">
                    <svg class="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                        <path class="text-slate-800" stroke-width="3.5" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                        <path class="text-[#10B981]" stroke-dasharray="92, 100" stroke-width="3.5" stroke-linecap="round" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                    </svg>
                    <span class="absolute text-[9px] font-bold text-white">92%</span>
                </div>
            </div>
        </section>

        <!-- Banner com a Imagem de Fundo Hero (Drones/Pivôs) -->
        <section class="relative h-60 w-full overflow-hidden rounded-3xl bg-slate-900 border border-[#1E293B]/30 shadow-sm flex items-end p-6">
            <!-- Background realístico do campo rural -->
            <img src="https://images.unsplash.com/photo-1592982537447-744077110b84?auto=format&fit=crop&q=80&w=1200" alt="Vista Aérea Lavoura" class="absolute inset-0 w-full h-full object-cover opacity-40 brightness-75">
            <div class="absolute inset-0 bg-gradient-to-t from-[#090D16] via-transparent to-transparent"></div>
            
            <div class="relative flex items-center space-x-3 bg-[#090D16]/80 backdrop-blur-md px-4 py-2.5 rounded-2xl border border-[#1E293B]/40 max-w-md">
                <div class="text-[#10B981]">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.77.946.669.752 1.109 1.706 1.205 2.76.023.25.034.503.034.757a7.969 7.969 0 01-.416 2.547h.81a1 1 0 00.993-.883l.5-4.375a1 1 0 00-.535-.98l-.371-.186zm-1.876.549A5.968 5.968 0 009.023 2c-1.157 0-2.23.328-3.14.895l-.37.185a1 1 0 00-.536.98l.5 4.375a1 1 0 00.993.883h.81A7.97 7.97 0 017 6.77c0-.254.01-.506.034-.756.096-1.054.536-2.008 1.205-2.76a1 1 0 00-.77-.946zM2 13a1 1 0 011-1h14a1 1 0 110 2H3a1 1 0 01-1-1zm1 3a1 1 0 100 2h14a1 1 0 100-2H3z" clip-rule="evenodd"></path></svg>
                </div>
                <div>
                    <h4 class="text-xs font-bold text-white">Monitoramento em Tempo Real</h4>
                    <p class="text-[10px] text-slate-400 mt-0.5">Dados coletados e atualizados via rede IoT</p>
                </div>
            </div>
        </section>

        <!-- Grid de Cards Estilizados (Indicadores Críticos) -->
        <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            
            <!-- Card 1: Temperatura -->
            <div class="bg-[#0D1321] border border-[#1E293B]/50 rounded-2xl p-5 flex flex-col justify-between space-y-4">
                <div class="flex items-center justify-between">
                    <div class="p-2 bg-[#F97316]/10 text-[#F97316] rounded-xl border border-[#F97316]/20">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2"></path></svg>
                    </div>
                    <span class="text-[10px] font-bold text-[#10B981] flex items-center gap-1">
                        <span class="w-1 h-1 rounded-full bg-[#10B981]"></span> Normal
                    </span>
                </div>
                <div>
                    <span class="text-xs font-medium text-slate-400">Temperatura Ambiente</span>
                    <h3 class="text-3xl font-bold text-white mt-1">28.5<span class="text-sm font-medium text-slate-400"> °C</span></h3>
                </div>
                <div class="space-y-1">
                    <div class="w-full bg-slate-800 h-1 rounded-full overflow-hidden">
                        <div class="bg-[#10B981] h-full w-[52%]"></div>
                    </div>
                    <div class="flex justify-between text-[10px] font-mono text-slate-500">
                        <span>18°C</span>
                        <span>38°C</span>
                    </div>
                </div>
                <div class="flex justify-between items-center pt-1 border-t border-slate-800 text-[10px] font-medium text-slate-500">
                    <span class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-slate-400"></span> MQTT</span>
                    <span>2 min atrás</span>
                </div>
            </div>

            <!-- Card 2: Umidade do Solo -->
            <div class="bg-[#0D1321] border border-[#1E293B]/50 rounded-2xl p-5 flex flex-col justify-between space-y-4">
                <div class="flex items-center justify-between">
                    <div class="p-2 bg-blue-500/10 text-blue-400 rounded-xl border border-blue-500/20">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
                    </div>
                    <span class="text-[10px] font-bold text-[#10B981] flex items-center gap-1">
                        <span class="w-1 h-1 rounded-full bg-[#10B981]"></span> Normal
                    </span>
                </div>
                <div>
                    <span class="text-xs font-medium text-slate-400">Umidade do Solo</span>
                    <h3 class="text-3xl font-bold text-white mt-1">62.3<span class="text-sm font-medium text-slate-400"> %</span></h3>
                </div>
                <div class="space-y-1">
                    <div class="w-full bg-slate-800 h-1 rounded-full overflow-hidden">
                        <div class="bg-[#10B981] h-full w-[65%]"></div>
                    </div>
                    <div class="flex justify-between text-[10px] font-mono text-slate-500">
                        <span>30%</span>
                        <span>90%</span>
                    </div>
                </div>
                <div class="flex justify-between items-center pt-1 border-t border-slate-800 text-[10px] font-medium text-slate-500">
                    <span class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-slate-400"></span> LoRa</span>
                    <span>5 min atrás</span>
                </div>
            </div>

            <!-- Card 3: Pluviometria -->
            <div class="bg-[#0D1321] border border-[#1E293B]/50 rounded-2xl p-5 flex flex-col justify-between space-y-4">
                <div class="flex items-center justify-between">
                    <div class="p-2 bg-cyan-500/10 text-cyan-400 rounded-xl border border-cyan-500/20">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path></svg>
                    </div>
                    <span class="text-[10px] font-bold text-[#10B981] flex items-center gap-1">
                        <span class="w-1 h-1 rounded-full bg-[#10B981]"></span> Normal
                    </span>
                </div>
                <div>
                    <span class="text-xs font-medium text-slate-400">Pluviometria</span>
                    <h3 class="text-3xl font-bold text-white mt-1">2.4<span class="text-sm font-medium text-slate-400"> mm</span></h3>
                </div>
                <div class="space-y-1">
                    <div class="w-full bg-slate-800 h-1 rounded-full overflow-hidden">
                        <div class="bg-slate-600 h-full w-[8%]"></div>
                    </div>
                    <div class="flex justify-between text-[10px] font-mono text-slate-500">
                        <span>0mm</span>
                        <span>50mm</span>
                    </div>
                </div>
                <div class="flex justify-between items-center pt-1 border-t border-slate-800 text-[10px] font-medium text-slate-500">
                    <span class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-slate-400"></span> LoRa</span>
                    <span>10 min atrás</span>
                </div>
            </div>

            <!-- Card 4: Nível do Reservatório -->
            <div class="bg-[#0D1321] border border-[#1E293B]/50 rounded-2xl p-5 flex flex-col justify-between space-y-4">
                <div class="flex items-center justify-between">
                    <div class="p-2 bg-[#F59E0B]/10 text-[#F59E0B] rounded-xl border border-[#F59E0B]/20">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
                    </div>
                    <span class="text-[10px] font-bold text-[#F59E0B] flex items-center gap-1">
                        <span class="w-1 h-1 rounded-full bg-[#F59E0B] animate-pulse"></span> Atenção
                    </span>
                </div>
                <div>
                    <span class="text-xs font-medium text-slate-400">Nível do Reservatório</span>
                    <h3 class="text-3xl font-bold text-white mt-1">74.8<span class="text-sm font-medium text-slate-400"> %</span></h3>
                </div>
                <div class="space-y-1">
                    <div class="w-full bg-slate-800 h-1 rounded-full overflow-hidden">
                        <div class="bg-[#F59E0B] h-full w-[74.8%]"></div>
                    </div>
                    <div class="flex justify-between text-[10px] font-mono text-slate-500">
                        <span>20%</span>
                        <span>100%</span>
                    </div>
                </div>
                <div class="flex justify-between items-center pt-1 border-t border-slate-800 text-[10px] font-medium text-slate-500">
                    <span class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-slate-400"></span> Zigbee</span>
                    <span>1 min atrás</span>
                </div>
            </div>

        </section>

        <!-- Seção de Análise Analítica (Gráficos) -->
        <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            <!-- Bloco Esquerdo: Histórico Temperatura -->
            <div class="bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-5 shadow-sm">
                <div class="flex items-center justify-between mb-4">
                    <span class="text-xs font-semibold text-white">Temperatura</span>
                    <span class="text-[11px] text-slate-400 font-medium">Últimas 24h <strong class="text-white ml-1">28.5°C</strong></span>
                </div>
                <div id="chart-temperature"></div>
            </div>

            <!-- Bloco Direito: Histórico Umidade do Solo -->
            <div class="bg-[#0D1321] border border-[#1E293B]/40 rounded-2xl p-5 shadow-sm">
                <div class="flex items-center justify-between mb-4">
                    <span class="text-xs font-semibold text-white">Umidade do Solo</span>
                    <span class="text-[11px] text-slate-400 font-medium">Últimas 24h <strong class="text-white ml-1">62.3%</strong></span>
                </div>
                <div id="chart-humidity"></div>
            </div>

        </section>
        
<!-- 2. CONTEÚDO PRINCIPAL DIREITO -->
    <main class="flex-1 p-8 space-y-6 overflow-y-auto">
        
        <!-- Bloco Principal de Equipamentos IoT -->
        <section class="bg-[#0D1321] border border-[#1E293B]/40 rounded-3xl p-6 shadow-sm space-y-4">
            
            <!-- Cabeçalho do Bloco -->
            <div class="flex items-center justify-between pb-2 border-b border-[#1E293B]/30">
                <h3 class="text-base font-semibold text-white tracking-tight">Equipamentos IoT</h3>
                <div class="flex items-center space-x-4 text-xs font-medium">
                    <span class="flex items-center gap-1.5 text-slate-400">
                        <span class="w-1.5 h-1.5 rounded-full bg-[#10B981]"></span> 4 online
                    </span>
                    <span class="flex items-center gap-1.5 text-slate-400">
                        <span class="w-1.5 h-1.5 rounded-full bg-rose-500"></span> 1 offline
                    </span>
                </div>
            </div>

            <!-- Lista de Dispositivos -->
            <div class="space-y-2">
                
                <!-- Dispositivo 1: Estação Meteorológica -->
                <div class="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-2xl bg-[#090D16]/40 border border-[#1E293B]/20 gap-4">
                    <div class="flex items-center space-x-4">
                        <div class="p-2.5 bg-[#10B981]/10 text-[#10B981] rounded-xl border border-[#10B981]/20">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path></svg>
                        </div>
                        <div>
                            <h4 class="text-sm font-semibold text-white">Estação Meteorológica A1</h4>
                            <p class="text-[11px] text-slate-500 font-medium">Setor Norte - Talhão 3</p>
                        </div>
                    </div>
                    <div class="flex items-center space-x-6 text-xs font-medium text-slate-400">
                        <span class="bg-[#10B981]/10 text-[#10B981] px-2.5 py-1 rounded-lg border border-[#10B981]/20 text-[10px] font-bold">Online</span>
                        <span class="flex items-center gap-1 font-mono text-[11px]">🪫 92%</span>
                        <span class="flex items-center gap-1 font-mono text-[11px]">📶 95%</span>
                        <span class="text-slate-500 font-normal text-[11px]">30s atrás</span>
                    </div>
                </div>

                <!-- Dispositivo 2: Sensor de Solo -->
                <div class="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-2xl bg-[#090D16]/40 border border-[#1E293B]/20 gap-4">
                    <div class="flex items-center space-x-4">
                        <div class="p-2.5 bg-[#10B981]/10 text-[#10B981] rounded-xl border border-[#10B981]/20">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
                        </div>
                        <div>
                            <h4 class="text-sm font-semibold text-white">Sensor de Solo B2</h4>
                            <p class="text-[11px] text-slate-500 font-medium">Setor Leste - Talhão 7</p>
                        </div>
                    </div>
                    <div class="flex items-center space-x-6 text-xs font-medium text-slate-400">
                        <span class="bg-[#10B981]/10 text-[#10B981] px-2.5 py-1 rounded-lg border border-[#10B981]/20 text-[10px] font-bold">Online</span>
                        <span class="flex items-center gap-1 font-mono text-[11px]">🪫 68%</span>
                        <span class="flex items-center gap-1 font-mono text-[11px]">📶 78%</span>
                        <span class="text-slate-500 font-normal text-[11px]">2min atrás</span>
                    </div>
                </div>

                <!-- Dispositivo 3: Controlador de Irrigação -->
                <div class="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-2xl bg-[#090D16]/40 border border-[#1E293B]/20 gap-4">
                    <div class="flex items-center space-x-4">
                        <div class="p-2.5 bg-[#10B981]/10 text-[#10B981] rounded-xl border border-[#10B981]/20">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
                        </div>
                        <div>
                            <h4 class="text-sm font-semibold text-white">Controlador de Irrigação C1</h4>
                            <p class="text-[11px] text-slate-500 font-medium">Setor Sul - Pivô Central</p>
                        </div>
                    </div>
                    <div class="flex items-center space-x-6 text-xs font-medium text-slate-400">
                        <span class="bg-[#10B981]/10 text-[#10B981] px-2.5 py-1 rounded-lg border border-[#10B981]/20 text-[10px] font-bold">Online</span>
                        <span class="flex items-center gap-1 font-mono text-[11px]">🪫 100%</span>
                        <span class="flex items-center gap-1 font-mono text-[11px]">📶 88%</span>
                        <span class="text-slate-500 font-normal text-[11px]">15s atrás</span>
                    </div>
                </div>

                <!-- Dispositivo 4: Gateway LoRa -->
                <div class="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-2xl bg-[#090D16]/40 border border-[#1E293B]/20 gap-4">
                    <div class="flex items-center space-x-4">
                        <div class="p-2.5 bg-[#10B981]/10 text-[#10B981] rounded-xl border border-[#10B981]/20">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 5h10a2 2 0 012 2v10a2 2 0 01-2 2H7a2 2 0 01-2-2V7a2 2 0 012-2z"></path></svg>
                        </div>
                        <div>
                            <h4 class="text-sm font-semibold text-white">Gateway LoRa D1</h4>
                            <p class="text-[11px] text-slate-500 font-medium">Torre Central</p>
                        </div>
                    </div>
                    <div class="flex items-center space-x-6 text-xs font-medium text-slate-400">
                        <span class="bg-[#10B981]/10 text-[#10B981] px-2.5 py-1 rounded-lg border border-[#10B981]/20 text-[10px] font-bold">Online</span>
                        <span class="flex items-center gap-1 font-mono text-[11px]">🪫 100%</span>
                        <span class="flex items-center gap-1 font-mono text-[11px]">📶 99%</span>
                        <span class="text-slate-500 font-normal text-[11px]">5s atrás</span>
                    </div>
                </div>

                <!-- Dispositivo 5: Sensor Pluviométrico (Offline) -->
                <div class="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-2xl bg-[#090D16]/40 border border-[#1E293B]/20 gap-4">
                    <div class="flex items-center space-x-4">
                        <div class="p-2.5 bg-rose-500/10 text-rose-400 rounded-xl border border-rose-500/20">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"></path></svg>
                        </div>
                        <div>
                            <h4 class="text-sm font-semibold text-white">Sensor Pluviométrico E1</h4>
                            <p class="text-[11px] text-slate-500 font-medium">Setor Oeste - Talhão 12</p>
                        </div>
                    </div>
                    <div class="flex items-center space-x-6 text-xs font-medium text-slate-400">
                        <span class="bg-rose-500/10 text-rose-400 px-2.5 py-1 rounded-lg border border-rose-500/20 text-[10px] font-bold">Offline</span>
                        <span class="flex items-center gap-1 font-mono text-[11px] text-rose-400/80">🪫 12%</span>
                        <span class="flex items-center gap-1 font-mono text-[11px] text-rose-400/80">📶 0%</span>
                        <span class="text-slate-500 font-normal text-[11px]">3h atrás</span>
                    </div>
                </div>

                <!-- Dispositivo 6: Câmera de Monitoramento (Manutenção) -->
                <div class="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-2xl bg-[#090D16]/40 border border-[#1E293B]/20 gap-4">
                    <div class="flex items-center space-x-4">
                        <div class="p-2.5 bg-amber-500/10 text-amber-400 rounded-xl border border-amber-500/20">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path></svg>
                        </div>
                        <div>
                            <h4 class="text-sm font-semibold text-white">Câmera de Monitoramento F1</h4>
                            <p class="text-[11px] text-slate-500 font-medium">Entrada Principal</p>
                        </div>
                    </div>
                    <div class="flex items-center space-x-6 text-xs font-medium text-slate-400">
                        <span class="bg-amber-500/10 text-amber-400 px-2.5 py-1 rounded-lg border border-amber-500/20 text-[10px] font-bold">Manutenção</span>
                        <span class="flex items-center gap-1 font-mono text-[11px]">🪫 100%</span>
                        <span class="flex items-center gap-1 font-mono text-[11px]">📶 45%</span>
                        <span class="text-slate-500 font-normal text-[11px]">1h atrás</span>
                    </div>
                </div>

            </div>
        </section>

        <!-- 3. CARDS INFERIORES INSTITUCIONAIS -->
        <section class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <!-- Card 1: Sensores no Campo -->
            <div class="relative h-44 rounded-2xl overflow-hidden bg-slate-900 border border-[#1E293B]/30 shadow-sm flex items-end p-5 group">
                <img src="https://images.unsplash.com/photo-1560493458-3e5b17a6212e?auto=format&fit=crop&q=80&w=600" alt="Sensores" class="absolute inset-0 w-full h-full object-cover opacity-30 brightness-75 group-hover:scale-105 transition duration-500">
                <div class="absolute inset-0 bg-gradient-to-t from-[#090D16] via-transparent to-transparent"></div>
                <div class="relative">
                    <h4 class="text-sm font-bold text-white">Sensores no Campo</h4>
                    <p class="text-[11px] text-slate-400 mt-0.5">Comunicação direta via redes estáveis LoRa e MQTT</p>
                </div>
            </div>

            <!-- Card 2: Estufas Automatizadas -->
            <div class="relative h-44 rounded-2xl overflow-hidden bg-slate-900 border border-[#1E293B]/30 shadow-sm flex items-end p-5 group">
                <img src="https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&q=80&w=600" alt="Estufas" class="absolute inset-0 w-full h-full object-cover opacity-30 brightness-75 group-hover:scale-105 transition duration-500">
                <div class="absolute inset-0 bg-gradient-to-t from-[#090D16] via-transparent to-transparent"></div>
                <div class="relative">
                    <h4 class="text-sm font-bold text-white">Estufas Automatizadas</h4>
                    <p class="text-[11px] text-slate-400 mt-0.5">Irrigação e controle microclimático inteligente via Zigbee</p>
                </div>
            </div>
        </section>

        <!-- Rodapé Atoms -->
        <footer class="flex justify-end pt-2 text-[10px] text-slate-600 font-medium">
            <span>Made by <strong class="text-slate-400 font-semibold">Atoms</strong></span>
        </footer>

    </main>        




    <!-- Rodapé de Crédito Discreto -->
    <footer class="flex justify-end pt-2 text-[10px] text-slate-600 font-medium">
        <span>Made by <strong class="text-slate-400 font-semibold">Atoms</strong></span>
    </footer>
    </main>
  </q-page>
</template>


<script setup></script>

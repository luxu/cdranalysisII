<template>
  <div
    class="relative h-44 rounded-2xl overflow-hidden bg-slate-900 border border-[#1E293B]/30 shadow-sm flex items-end p-5 group"
  >
    <img
      :src="image"
      :alt="title"
      class="absolute inset-0 w-full h-full object-cover opacity-30 brightness-75 group-hover:scale-105 transition duration-500"
    />
    <div
      class="absolute inset-0 bg-gradient-to-t from-[#090D16] via-transparent to-transparent"
    />
    <div class="relative">
      <h4 class="text-sm font-bold text-white">{{ title }}</h4>
      <p class="text-[11px] text-slate-400 mt-0.5">{{ description }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  image: { type: String, required: true },
  title: { type: String, required: true },
  description: { type: String, required: true }
})
</script>

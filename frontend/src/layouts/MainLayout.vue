<template>
  <q-layout view="lHh Lpr lFf">
    <AppSidebar :alert-count="3" />

    <q-page-container>
      <router-view />
      <footer
        class="flex justify-end pt-2 pb-4 pr-8 text-[10px] text-slate-600 font-medium"
      >
        <span
          >Made by
          <strong class="text-slate-400 font-semibold">Atoms</strong></span
        >
      </footer>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import AppSidebar from '@/components/AppSidebar.vue'
</script>

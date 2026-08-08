<template>
  <q-layout view="lHh Lpr lFf">
    <AppSidebar :alert-count="3" />

    <q-page-container>
      <router-view />
      <footer
        class="flex justify-end pt-2 pb-4 pr-8 text-[10px] text-slate-600 font-medium"
      >
      </footer>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import AppSidebar from '@/components/AppSidebar.vue'
</script>

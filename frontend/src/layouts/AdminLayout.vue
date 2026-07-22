<template>
  <q-layout view="lHh Lpr lFf">
    <AdminSidebar />

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import AdminSidebar from '@/components/AdminSidebar.vue'
</script>

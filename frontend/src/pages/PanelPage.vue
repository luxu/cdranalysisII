<template>
  <AdminPanel v-if="canAccessAdmin" />
  <UserPanel v-else />
</template>

<script setup>
import useAuth from '@/composables/useAuth'
// import AdminPanel from './AdminPanel.vue'
import UserPanel from './UserPanel.vue'

const { canAccessAdmin } = useAuth()
</script>

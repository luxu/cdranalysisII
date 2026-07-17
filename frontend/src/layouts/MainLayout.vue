<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header>Menu</q-item-label>

        <q-item
          v-for="item in linksList"
          :key="item.label"
          clickable
          :to="item.link"
          exact
        >
          <q-item-section v-if="item.icon" avatar>
            <q-icon :name="item.icon" />
          </q-item-section>

          <q-item-section>
            <q-item-label>{{ item.label }}</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import EssentialLink from '@/components/EssentialLink.vue'

const linksList = [
  {
    label: 'Home',
    caption: 'Home',
    icon: 'home',
    link: '/'
  },
  {
    label: 'Profile',
    caption: 'Profile',
    icon: 'school',
    link: '/profile'
  },
  {
    label: 'Device',
    caption: 'Device',
    icon: 'devices',
    link: '/device'
  },
  {
    label: 'Organization',
    caption: 'Organization',
    icon: 'business',
    link: '/organization'
  },
  {
    label: 'Customer',
    caption: 'Customer',
    icon: 'people',
    link: '/customer'
  },
  {
    label: 'MNO',
    caption: 'MNO',
    icon: 'cell_tower',
    link: '/mno'
  },
  {
    label: 'NetworkProvider',
    caption: 'NetworkProvider',
    icon: 'router',
    link: '/networkprovider'
  },
  {
    label: 'PricePlan',
    caption: 'PricePlan',
    icon: 'sell',
    link: '/priceplan'
  },
  {
    label: 'Thing',
    caption: 'Thing',
    icon: 'memory',
    link: '/thing'
  },
  {
    label: 'Session',
    caption: 'Session',
    icon: 'sync_alt',
    link: '/session'
  },
  {
    label: 'XLSX',
    caption: 'XLSX',
    icon: 'file_upload',
    link: '/xlsx'
  }
]

const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>

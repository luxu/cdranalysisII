<template>
  <q-page padding>
    <div class="flex items-center justify-between q-mb-md">
      <h1 class="text-h5 text-weight-bold">Sessões</h1>
    </div>
    <q-table
      v-model:pagination="pagination"
      :rows="rows"
      :columns="columns"
      row-key="id"
      :loading="loading"
      @request="onRequest"
    >
      <template v-slot:body-cell-status="props">
        <q-td :props="props">
          <q-badge :color="props.value ? 'positive' : 'negative'">
            {{ props.value ? 'Sim' : 'Não' }}
          </q-badge>
        </q-td>
      </template>
    </q-table>
  </q-page>
</template>

<script setup>
import { columns } from './table'
import sessionService from '@/services/session'
import useCrudList from '@/composables/useCrudList'

const { rows, loading, pagination, onRequest } = useCrudList(sessionService, {
  entityLabel: 'Sessão'
})
</script>

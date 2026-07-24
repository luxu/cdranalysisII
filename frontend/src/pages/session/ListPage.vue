<template>
  <q-page padding>
    <div class="flex items-center justify-between q-mb-md">
      <h1 class="text-h5 text-weight-bold">Sessões</h1>
    </div>

    <q-card class="q-mb-md">
      <q-card-section class="q-py-sm">
        <div class="row q-col-gutter-sm items-center">
          <div class="col-12 col-sm-4">
            <q-input
              v-model="search"
              dense
              outlined
              placeholder="Buscar por Session ID, IMSI, MSISDN ou Thing..."
              debounce="300"
              clearable
              @clear="applyFilters"
            >
              <template v-slot:prepend>
                <q-icon name="search" />
              </template>
            </q-input>
          </div>
          <div class="col-6 col-sm-3">
            <q-input
              v-model="startDate"
              dense
              outlined
              type="date"
              label="Data início"
              debounce="300"
              @update:model-value="applyFilters"
            />
          </div>
          <div class="col-6 col-sm-3">
            <q-input
              v-model="endDate"
              dense
              outlined
              type="date"
              label="Data fim"
              debounce="300"
              @update:model-value="applyFilters"
            />
          </div>
          <div class="col-12 col-sm-2">
            <q-btn
              flat
              dense
              color="grey"
              label="Limpar"
              icon="clear_all"
              @click="clearFilters"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>

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
import { ref } from 'vue'
import { columns } from './table'
import sessionService from '@/services/session'
import useCrudList from '@/composables/useCrudList'

const { rows, loading, pagination, fetchRows, onRequest } = useCrudList(
  sessionService,
  { entityLabel: 'Sessão', rowsPerPage: 10 }
)

const search = ref('')
const startDate = ref('')
const endDate = ref('')

const buildParams = () => {
  const params = {}
  if (search.value) params.search = search.value
  if (startDate.value) params.start_date = startDate.value
  if (endDate.value) params.end_date = endDate.value
  return params
}

const applyFilters = () => fetchRows(1, buildParams())

const clearFilters = () => {
  search.value = ''
  startDate.value = ''
  endDate.value = ''
  fetchRows(1)
}
</script>

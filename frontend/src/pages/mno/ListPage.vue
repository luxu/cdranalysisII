<template>
  <q-page padding>
    <h1 class="text-h2 text-center">MNO List</h1>
    <q-btn
      color="primary"
      label="Add MNO"
      icon="add"
      :to="{ name: 'form-mno' }"
    />
    <q-table
      v-model:pagination="pagination"
      :rows="rows"
      :columns="columns"
      row-key="id"
      :loading="loading"
      @request="onRequest"
    >
      <template v-slot:body-cell-actions="props">
        <q-td :props="props" class="q-gutter-x-sm">
          <q-btn
            icon="mdi-pencil-outline"
            color="info"
            dense
            size="sm"
            @click="handlerEdit(props.row)"
          >
            <q-tooltip> Edit </q-tooltip>
          </q-btn>
          <q-btn
            icon="mdi-delete-outline"
            color="negative"
            dense
            size="sm"
            @click="handlerRemove(props.row)"
          >
            <q-tooltip> Delete </q-tooltip>
          </q-btn>
        </q-td>
      </template>
    </q-table>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useRouter } from 'vue-router'
import { columns } from './table'
import mnoService from '@/services/mno'
import useCrudList from '@/composables/useCrudList'

export default defineComponent({
  setup() {
    const router = useRouter()

    const { rows, loading, pagination, onRequest, confirmRemove } = useCrudList(
      mnoService,
      { entityLabel: 'MNO' }
    )

    const handlerEdit = (item: any) => {
      router.push({
        name: 'form-mno',
        params: { id: item.id }
      })
    }

    const handlerRemove = (item: any) => confirmRemove(item, item.mnoname)

    return {
      rows,
      columns,
      loading,
      pagination,
      onRequest,
      handlerEdit,
      handlerRemove
    }
  }
})
</script>

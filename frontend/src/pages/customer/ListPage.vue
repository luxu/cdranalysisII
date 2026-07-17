<template>
  <q-page padding>
    <h1 class="text-h2 text-center">Customer List</h1>
    <q-btn
      color="primary"
      label="Add Customer"
      icon="add"
      :to="{ name: 'form-customer' }"
    />
    <q-table :rows="rows" :columns="columns" row-key="id">
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
import { defineComponent, ref } from 'vue'
import { columns } from './table'
import { useRouter } from 'vue-router'

export default defineComponent({
  setup() {
    const router = useRouter()

    const rows = ref([
      {
        id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
        customerid: 'cid_4363b0be-4d72-49fd-995b-51a5ba2598e1',
        customername: 'SOLIS - OPERADORA AGRO',
        organization: 'Solis',
        organization_name: 'Solis'
      },
      {
        id: 'b2c3d4e5-f6a7-8901-bcde-f12345678901',
        customerid: 'cid_57afa6a5-a642-4d01-92f8-87880964264c',
        customername: 'VERACRUZ',
        organization: 'SolisTower',
        organization_name: 'SolisTower'
      }
    ])

    const handlerEdit = (item: any) => {
      router.push({
        name: 'form-customer',
        params: { id: item.id }
      })
    }

    const handlerRemove = (item: any) => {
      console.log('Removing customer:', item.id)
    }

    return {
      rows,
      columns,
      handlerEdit,
      handlerRemove
    }
  }
})
</script>

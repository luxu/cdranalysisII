<template>
  <q-page padding>
    <h1 class="text-h2 text-center">NetworkProvider List</h1>
    <q-btn
      color="primary"
      label="Add NetworkProvider"
      icon="add"
      :to="{ name: 'form-networkprovider' }"
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
        networkproviderid:
          'NetworkProviderId_57afa6a5-a642-4d01-92f8-87880964264c',
        networkprovidername: 'CBRS 315010 Solis',
        customer: 'SOLIS - OPERADORA AGRO',
        customer_name: 'SOLIS - OPERADORA AGRO'
      },
      {
        id: 'b2c3d4e5-f6a7-8901-bcde-f12345678901',
        networkproviderid:
          'NetworkProviderId_8540c013-1501-41d4-9c9b-2feea91c1473',
        networkprovidername: 'CBRS 72472 Veracruz',
        customer: 'VERACRUZ',
        customer_name: 'VERACRUZ'
      }
    ])

    const handlerEdit = (item: any) => {
      router.push({
        name: 'form-networkprovider',
        params: { id: item.id }
      })
    }

    const handlerRemove = (item: any) => {
      console.log('Removing networkprovider:', item.id)
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

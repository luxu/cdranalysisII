<template>
  <q-page padding>
    <h1 class="text-h2 text-center">Device List</h1>
    <q-btn
      color="primary"
      label="Add Device"
      icon="add"
      :to="{ name: 'form-device' }"
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
        thing: 'Thing 1',
        thing_name: 'Thing 1',
        iccid: '8955000000000000001',
        imsi: '724000000000001',
        msisdn: '5511999990001',
        mei: '356938035643801'
      },
      {
        id: 'b2c3d4e5-f6a7-8901-bcde-f12345678901',
        thing: 'Thing 2',
        thing_name: 'Thing 2',
        iccid: '8955000000000000002',
        imsi: '724000000000002',
        msisdn: '5511999990002',
        mei: '356938035643802'
      }
    ])

    const handlerEdit = (item: any) => {
      router.push({
        name: 'form-device',
        params: { id: item.id }
      })
    }

    return {
      rows,
      columns,
      handlerEdit
    }
  }
})
</script>

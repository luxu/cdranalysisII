<template>
  <q-page padding>
    <h1 class="text-h2 text-center">Session List</h1>
    <q-btn
      color="primary"
      label="Add Session"
      icon="add"
      :to="{ name: 'form-session' }"
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
        device: 'ICCID 8997211425012500335',
        device_name: 'ICCID 8997211425012500335',
        sessionid: '765',
        imsi: '315010012500335',
        sessioncreatetime: '2026-01-14 09:25:37',
        realusage: '62384095',
        uom: 'bytes'
      },
      {
        id: 'b2c3d4e5-f6a7-8901-bcde-f12345678901',
        device: 'ICCID 8997211425012500335',
        device_name: 'ICCID 8997211425012500335',
        sessionid: '766',
        imsi: '315010012500335',
        sessioncreatetime: '2026-01-14 09:27:23',
        realusage: '75986',
        uom: 'bytes'
      }
    ])

    const handlerEdit = (item: any) => {
      router.push({
        name: 'form-session',
        params: { id: item.id }
      })
    }

    const handlerRemove = (item: any) => {
      console.log('Removing session:', item.id)
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

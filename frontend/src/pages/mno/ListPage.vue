<template>
  <q-page padding>
    <h1 class="text-h2 text-center">MNO List</h1>
    <q-btn
      color="primary"
      label="Add MNO"
      icon="add"
      :to="{ name: 'form-mno' }"
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
        mnoid: 'MNOId_48d1f9c1-283a-45ea-8f09-50a75f8f80b9',
        mnoname: 'CBRS 72472',
        organization: 'Solis',
        organization_name: 'Solis'
      },
      {
        id: 'b2c3d4e5-f6a7-8901-bcde-f12345678901',
        mnoid: 'MNOId_8540c013-1501-41d4-9c9b-2feea91c1473',
        mnoname: 'Vivo',
        organization: 'SolisTower',
        organization_name: 'SolisTower'
      }
    ])

    const handlerEdit = (item: any) => {
      router.push({
        name: 'form-mno',
        params: { id: item.id }
      })
    }

    const handlerRemove = (item: any) => {
      console.log('Removing mno:', item.id)
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

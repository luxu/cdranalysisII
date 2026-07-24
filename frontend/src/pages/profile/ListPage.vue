<template>
  <q-page padding>
    <h1 class="text-h2 text-center">Lista de Usuários</h1>
    <q-btn
      color="primary"
      label="Adicionar Usuário"
      icon="add"
      :to="formRoute()"
    />
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
      <template v-slot:body-cell-actions="props">
        <q-td :props="props" class="q-gutter-x-sm">
          <q-btn
            icon="mdi-pencil-outline"
            color="info"
            dense
            size="sm"
            @click="handlerEdit(props.row)"
          >
            <q-tooltip> Editar </q-tooltip>
          </q-btn>
          <q-btn
            icon="mdi-delete-outline"
            color="negative"
            dense
            size="sm"
            @click="handlerRemove(props.row)"
          >
            <q-tooltip> Excluir </q-tooltip>
          </q-btn>
        </q-td>
      </template>
    </q-table>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { columns } from './table'
import profileService from '@/services/profile'
import useCrudList from '@/composables/useCrudList'

export default defineComponent({
  setup() {
    const router = useRouter()
    const route = useRoute()

    const { rows, loading, pagination, onRequest, confirmRemove } = useCrudList(
      profileService,
      { entityLabel: 'Perfil' }
    )

    const isAdmin = () => route.path.startsWith('/admin')

    const formRoute = id => {
      if (isAdmin()) {
        return id ? `/admin/profile-form/${id}` : '/admin/profile-form'
      }
      return id
        ? { name: 'form-profile', params: { id } }
        : { name: 'form-profile' }
    }

    const handlerEdit = item => {
      router.push(formRoute(item.id))
    }

    const handlerRemove = item => confirmRemove(item, item.name)

    return {
      rows,
      columns,
      loading,
      pagination,
      onRequest,
      formRoute,
      handlerEdit,
      handlerRemove
    }
  }
})
</script>

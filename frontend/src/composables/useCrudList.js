import { onMounted, ref } from 'vue'
import { useQuasar } from 'quasar'

// Composable para telas de lista: busca paginada (DRF PageNumberPagination)
// e remoção com diálogo de confirmação.
// Uso: const { rows, loading, pagination, onRequest, confirmRemove } =
//        useCrudList(organizationService, { entityLabel: 'Organization' })
export default function useCrudList(
  service,
  { entityLabel = 'registro', rowsPerPage: initialRowsPerPage } = {}
) {
  const $q = useQuasar()
  const rows = ref([])
  const loading = ref(false)
  const pagination = ref({
    page: 1,
    rowsPerPage: initialRowsPerPage || 50,
    rowsNumber: 0
  })

  const fetchRows = async (page = pagination.value.page, extraParams = {}) => {
    loading.value = true
    try {
      const params = {
        page,
        page_size: pagination.value.rowsPerPage,
        ...extraParams
      }
      const data = await service.list(params)
      rows.value = data.results
      pagination.value.page = page
      pagination.value.rowsNumber = data.count
    } catch (error) {
      $q.notify({ type: 'negative', message: error.friendlyMessage })
    } finally {
      loading.value = false
    }
  }

  // Handler do @request do q-table (mudança de página)
  const onRequest = props => fetchRows(props.pagination.page)

  const confirmRemove = (item, description) => {
    $q.dialog({
      title: 'Confirmar exclusão',
      message: `Remover ${entityLabel} "${description}"?`,
      cancel: true,
      persistent: true
    }).onOk(async () => {
      try {
        await service.remove(item.id)
        $q.notify({ type: 'positive', message: 'Removido com sucesso' })
        fetchRows()
      } catch (error) {
        $q.notify({ type: 'negative', message: error.friendlyMessage })
      }
    })
  }

  onMounted(() => fetchRows(1))

  return { rows, loading, pagination, fetchRows, onRequest, confirmRemove }
}

import { onMounted, ref } from 'vue'
import { useQuasar } from 'quasar'

// Carrega opções de um q-select (FK) a partir de um service CRUD.
// Retorna um ref de array com os registros (results da paginação DRF).
export default function useOptions(service) {
  const $q = useQuasar()
  const options = ref([])

  onMounted(async () => {
    try {
      const data = await service.list()
      options.value = data.results
    } catch (error) {
      $q.notify({ type: 'negative', message: error.friendlyMessage })
    }
  })

  return options
}

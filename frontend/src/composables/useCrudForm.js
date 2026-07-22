import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'

export default function useCrudForm(
  service,
  { listRoute, initialForm, mapIn = null }
) {
  const $q = useQuasar()
  const router = useRouter()
  const route = useRoute()

  const form = ref({ ...initialForm })
  const errors = ref({})
  const loading = ref(false)

  const isUpdate = computed(() => !!route.params.id)

  const resolvedListRoute = computed(() => {
    const meta = route.meta?.listRoute
    return meta || listRoute
  })

  const hasError = field => !!errors.value[field]

  const fieldError = field => {
    const error = errors.value[field]
    return Array.isArray(error) ? error.join(' ') : error || ''
  }

  onMounted(async () => {
    if (!isUpdate.value) return
    loading.value = true
    try {
      const data = await service.get(route.params.id)
      const source = mapIn ? mapIn(data) : data
      for (const key of Object.keys(initialForm)) {
        form.value[key] = source[key] ?? initialForm[key]
      }
    } catch (error) {
      $q.notify({ type: 'negative', message: error.friendlyMessage })
    } finally {
      loading.value = false
    }
  })

  const onSubmit = async () => {
    errors.value = {}
    loading.value = true
    try {
      if (isUpdate.value) {
        await service.update(route.params.id, form.value)
      } else {
        await service.create(form.value)
      }
      const target = resolvedListRoute.value
      router.push(
        typeof target === 'string' && target.startsWith('/')
          ? target
          : { name: target }
      )
    } catch (error) {
      if (error.response?.status === 400) {
        errors.value = error.response.data
        const nonField = error.response.data?.non_field_errors
        if (nonField) {
          $q.notify({
            type: 'negative',
            message: [].concat(nonField).join(' ')
          })
        }
      } else {
        $q.notify({ type: 'negative', message: error.friendlyMessage })
      }
    } finally {
      loading.value = false
    }
  }

  return { form, loading, isUpdate, hasError, fieldError, onSubmit }
}

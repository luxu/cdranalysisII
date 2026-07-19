<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex flex-center bg-grey-3">
        <q-card class="q-pa-lg" style="width: 400px">
          <q-card-section class="text-center q-mb-md">
            <div class="text-h5 text-weight-bold">CDR Analysis</div>
            <div class="text-subtitle2 text-grey-6">Entrar no sistema</div>
          </q-card-section>

          <q-card-section>
            <q-form class="q-gutter-md" @submit.prevent="handleLogin">
              <q-input
                v-model="email"
                filled
                label="E-mail"
                type="email"
                :error="hasError('email')"
                :error-message="fieldError('email')"
              />

              <q-input
                v-model="password"
                filled
                label="Senha"
                type="password"
                :error="hasError('password')"
                :error-message="fieldError('password')"
              />

              <q-btn
                label="Entrar"
                type="submit"
                color="primary"
                class="full-width"
                :loading="loading"
              />
            </q-form>
          </q-card-section>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import useAuth from '@/composables/useAuth'

const router = useRouter()
const $q = useQuasar()
const { login } = useAuth()

const email = ref('admin@admin.com')
const password = ref('')
const loading = ref(false)
const errors = ref({})

const hasError = field => !!errors.value[field]

const fieldError = field => {
  const error = errors.value[field]
  return Array.isArray(error) ? error.join(' ') : error || ''
}

async function handleLogin() {
  errors.value = {}
  loading.value = true
  try {
    await login(email.value, password.value)
    router.push('/')
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
      $q.notify({
        type: 'negative',
        message: error.friendlyMessage || 'Erro ao entrar'
      })
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <q-page padding>
    <h1 class="text-h2 text-center"
      >{{ isUpdate ? 'Editar' : 'Novo' }} Perfil</h1
    >
    <div class="q-pa-md" style="max-width: 900px; margin: auto">
      <q-form class="q-gutter-md" @submit.prevent="onSubmit">
        <div class="row q-col-gutter-md">
          <template v-if="!isUpdate">
            <div class="col-12 col-sm-6 col-md-4">
              <q-input
                filled
                label="Email"
                type="email"
                v-model="form.email"
                :error="hasError('email')"
                :error-message="fieldError('email')"
              />
            </div>
            <div class="col-12 col-sm-6 col-md-4">
              <q-input
                filled
                label="Senha"
                type="password"
                v-model="form.password"
                :error="hasError('password')"
                :error-message="fieldError('password')"
              />
            </div>
          </template>
          <div class="col-12 col-sm-6 col-md-4">
            <q-input
              filled
              label="Nome"
              v-model="form.name"
              :error="hasError('name')"
              :error-message="fieldError('name')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-4">
            <q-input
              filled
              label="Celular"
              v-model="form.celular"
              :error="hasError('celular')"
              :error-message="fieldError('celular')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-4">
            <q-select
              filled
              label="Thing"
              v-model="form.thing"
              :options="thingOptions"
              option-label="thingsgroupname"
              option-value="id"
              emit-value
              map-options
              clearable
              :error="hasError('thing')"
              :error-message="fieldError('thing')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-4 flex items-center q-pt-lg">
            <q-toggle label="Ativo" v-model="form.status" color="primary" />
          </div>
        </div>
        <div>
          <q-btn
            label="Salvar"
            type="submit"
            color="primary"
            :loading="loading"
          />
        </div>
      </q-form>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import { useQuasar } from 'quasar'
import profileService from '@/services/profile'
import thingService from '@/services/thing'
import useCrudForm from '@/composables/useCrudForm'
import useOptions from '@/composables/useOptions'

export default defineComponent({
  setup() {
    const $q = useQuasar()

    const { form, loading, isUpdate, hasError, fieldError, onSubmit } =
      useCrudForm(profileService, {
        listRoute: 'profile',
        initialForm: {
          name: '',
          celular: '',
          thing: null,
          status: true,
          email: '',
          password: '123mudar'
        },
        onSuccess: isUpdate => {
          if (!isUpdate) {
            $q.notify({
              type: 'positive',
              message:
                'Perfil criado. Senha padrão: 123mudar. Envio de e-mail para troca de senha será implementado.'
            })
          }
        }
      })

    const thingOptions = useOptions(thingService)

    return {
      form,
      loading,
      isUpdate,
      thingOptions,
      hasError,
      fieldError,
      onSubmit
    }
  }
})
</script>

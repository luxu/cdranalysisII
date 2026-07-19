<template>
  <q-page padding>
    <h1 class="text-h2 text-center">NetworkProvider Page</h1>
    <div class="q-pa-md" style="max-width: 900px; margin: auto">
      <q-form class="q-gutter-md" @submit.prevent="onSubmit">
        <div class="row q-col-gutter-md">
          <div class="col-12 col-sm-6 col-md-3">
            <q-select
              filled
              label="Customer"
              v-model="form.customer"
              :options="customerOptions"
              option-label="customername"
              option-value="id"
              emit-value
              map-options
              :error="hasError('customer')"
              :error-message="fieldError('customer')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="NetworkProviderId"
              v-model="form.networkproviderid"
              :error="hasError('networkproviderid')"
              :error-message="fieldError('networkproviderid')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="NetworkProviderName"
              v-model="form.networkprovidername"
              :error="hasError('networkprovidername')"
              :error-message="fieldError('networkprovidername')"
            />
          </div>
        </div>
        <div class="col-12 col-sm-6 col-md-3">
          <q-btn
            label="Submit"
            type="submit"
            color="primary"
            :loading="loading"
          />
        </div>
      </q-form>
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import networkproviderService from '@/services/networkprovider'
import customerService from '@/services/customer'
import useCrudForm from '@/composables/useCrudForm'
import useOptions from '@/composables/useOptions'

export default defineComponent({
  setup() {
    const { form, loading, hasError, fieldError, onSubmit } = useCrudForm(
      networkproviderService,
      {
        listRoute: 'networkprovider',
        initialForm: {
          customer: null,
          networkproviderid: '',
          networkprovidername: ''
        }
      }
    )

    const customerOptions = useOptions(customerService)

    return {
      form,
      loading,
      customerOptions,
      hasError,
      fieldError,
      onSubmit
    }
  }
})
</script>

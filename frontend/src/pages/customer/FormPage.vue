<template>
  <q-page padding>
    <h1 class="text-h2 text-center">Customer Page</h1>
    <div class="q-pa-md" style="max-width: 900px; margin: auto">
      <q-form class="q-gutter-md" @submit.prevent="onSubmit">
        <div class="row q-col-gutter-md">
          <div class="col-12 col-sm-6 col-md-3">
            <q-select
              filled
              label="Organization"
              v-model="form.organization"
              :options="organizationOptions"
              option-label="orgname"
              option-value="id"
              emit-value
              map-options
              :error="hasError('organization')"
              :error-message="fieldError('organization')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="CustomerId"
              v-model="form.customerid"
              :error="hasError('customerid')"
              :error-message="fieldError('customerid')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="CustomerName"
              v-model="form.customername"
              :error="hasError('customername')"
              :error-message="fieldError('customername')"
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
import customerService from '@/services/customer'
import organizationService from '@/services/organization'
import useCrudForm from '@/composables/useCrudForm'
import useOptions from '@/composables/useOptions'

export default defineComponent({
  setup() {
    const { form, loading, hasError, fieldError, onSubmit } = useCrudForm(
      customerService,
      {
        listRoute: 'customer',
        initialForm: {
          organization: null,
          customerid: '',
          customername: ''
        }
      }
    )

    const organizationOptions = useOptions(organizationService)

    return {
      form,
      loading,
      organizationOptions,
      hasError,
      fieldError,
      onSubmit
    }
  }
})
</script>

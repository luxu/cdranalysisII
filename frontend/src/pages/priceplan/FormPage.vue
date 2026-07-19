<template>
  <q-page padding>
    <h1 class="text-h2 text-center">PricePlan Page</h1>
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
              label="PricePlanId"
              v-model="form.priceplanid"
              :error="hasError('priceplanid')"
              :error-message="fieldError('priceplanid')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="PricePlanName"
              v-model="form.priceplanname"
              :error="hasError('priceplanname')"
              :error-message="fieldError('priceplanname')"
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
import priceplanService from '@/services/priceplan'
import customerService from '@/services/customer'
import useCrudForm from '@/composables/useCrudForm'
import useOptions from '@/composables/useOptions'

export default defineComponent({
  setup() {
    const { form, loading, hasError, fieldError, onSubmit } = useCrudForm(
      priceplanService,
      {
        listRoute: 'priceplan',
        initialForm: {
          customer: null,
          priceplanid: '',
          priceplanname: ''
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

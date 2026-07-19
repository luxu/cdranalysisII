<template>
  <q-page padding>
    <h1 class="text-h2 text-center">Thing Page</h1>
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
              label="ThingsGroupId"
              v-model="form.thingsgroupid"
              :error="hasError('thingsgroupid')"
              :error-message="fieldError('thingsgroupid')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="ThingsGroupName"
              v-model="form.thingsgroupname"
              :error="hasError('thingsgroupname')"
              :error-message="fieldError('thingsgroupname')"
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
import thingService from '@/services/thing'
import customerService from '@/services/customer'
import useCrudForm from '@/composables/useCrudForm'
import useOptions from '@/composables/useOptions'

export default defineComponent({
  setup() {
    const { form, loading, hasError, fieldError, onSubmit } = useCrudForm(
      thingService,
      {
        listRoute: 'thing',
        initialForm: {
          customer: null,
          thingsgroupid: '',
          thingsgroupname: ''
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

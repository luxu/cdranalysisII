<template>
  <q-page padding>
    <h1 class="text-h2 text-center">Device Page</h1>
    <div class="q-pa-md" style="max-width: 900px; margin: auto">
      <q-form class="q-gutter-md" @submit.prevent="onSubmit">
        <div class="row q-col-gutter-md">
          <div class="col-12 col-sm-6 col-md-3">
            <q-select
              filled
              label="Thing"
              v-model="form.thing"
              :options="thingOptions"
              option-label="thingsgroupname"
              option-value="id"
              emit-value
              map-options
              :error="hasError('thing')"
              :error-message="fieldError('thing')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="ICCID (ID do cartão SIM)"
              v-model="form.iccid"
              :error="hasError('iccid')"
              :error-message="fieldError('iccid')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="IMSI (Internacional Mobile Subscriber Identity)"
              v-model="form.imsi"
              :error="hasError('imsi')"
              :error-message="fieldError('imsi')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="MEI (ID do aparelho)"
              v-model="form.mei"
              :error="hasError('mei')"
              :error-message="fieldError('mei')"
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
import deviceService from '@/services/device'
import thingService from '@/services/thing'
import useCrudForm from '@/composables/useCrudForm'
import useOptions from '@/composables/useOptions'

export default defineComponent({
  setup() {
    const { form, loading, hasError, fieldError, onSubmit } = useCrudForm(
      deviceService,
      {
        listRoute: 'device',
        initialForm: {
          thing: null,
          iccid: '',
          imsi: '',
          mei: ''
        }
      }
    )

    const thingOptions = useOptions(thingService)

    return {
      form,
      loading,
      thingOptions,
      hasError,
      fieldError,
      onSubmit
    }
  }
})
</script>

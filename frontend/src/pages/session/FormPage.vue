<template>
  <q-page padding>
    <h1 class="text-h2 text-center">Session Page</h1>
    <div class="q-pa-md" style="max-width: 900px; margin: auto">
      <q-form class="q-gutter-md" @submit.prevent="onSubmit">
        <div class="row q-col-gutter-md">
          <div class="col-12 col-sm-6 col-md-3">
            <q-select
              filled
              label="Device"
              v-model="form.device"
              :options="deviceOptions"
              option-label="iccid"
              option-value="id"
              emit-value
              map-options
              :error="hasError('device')"
              :error-message="fieldError('device')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="SessionId"
              v-model="form.sessionid"
              :error="hasError('sessionid')"
              :error-message="fieldError('sessionid')"
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
              label="SessionCreateTime"
              v-model="form.sessioncreatetime"
              type="datetime-local"
              :error="hasError('sessioncreatetime')"
              :error-message="fieldError('sessioncreatetime')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="RealUsage (consumo real)"
              v-model="form.realusage"
              :error="hasError('realusage')"
              :error-message="fieldError('realusage')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="UOM (Unidade de Medida, ex: MB, KB)"
              v-model="form.uom"
              :error="hasError('uom')"
              :error-message="fieldError('uom')"
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
import sessionService from '@/services/session'
import deviceService from '@/services/device'
import useCrudForm from '@/composables/useCrudForm'
import useOptions from '@/composables/useOptions'

export default defineComponent({
  setup() {
    const { form, loading, hasError, fieldError, onSubmit } = useCrudForm(
      sessionService,
      {
        listRoute: 'session',
        initialForm: {
          device: null,
          sessionid: '',
          imsi: '',
          sessioncreatetime: '',
          realusage: '',
          uom: ''
        },
        // API retorna ISO 8601 (ex.: 2026-01-14T09:25:37-03:00);
        // o input datetime-local aceita apenas YYYY-MM-DDTHH:mm
        mapIn: (data: any) => ({
          ...data,
          sessioncreatetime: data.sessioncreatetime?.slice(0, 16) || ''
        })
      }
    )

    const deviceOptions = useOptions(deviceService)

    return {
      form,
      loading,
      deviceOptions,
      hasError,
      fieldError,
      onSubmit
    }
  }
})
</script>

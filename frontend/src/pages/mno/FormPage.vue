<template>
  <q-page padding>
    <h1 class="text-h2 text-center">MNO Page</h1>
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
              label="MNOId"
              v-model="form.mnoid"
              :error="hasError('mnoid')"
              :error-message="fieldError('mnoid')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="MnoName"
              v-model="form.mnoname"
              :error="hasError('mnoname')"
              :error-message="fieldError('mnoname')"
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
import mnoService from '@/services/mno'
import organizationService from '@/services/organization'
import useCrudForm from '@/composables/useCrudForm'
import useOptions from '@/composables/useOptions'

export default defineComponent({
  setup() {
    const { form, loading, hasError, fieldError, onSubmit } = useCrudForm(
      mnoService,
      {
        listRoute: 'mno',
        initialForm: {
          organization: null,
          mnoid: '',
          mnoname: ''
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

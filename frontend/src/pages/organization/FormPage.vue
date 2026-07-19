<template>
  <q-page padding>
    <h1 class="text-h2 text-center">Organization Page</h1>
    <div class="q-pa-md" style="max-width: 900px; margin: auto">
      <q-form class="q-gutter-md" @submit.prevent="onSubmit">
        <div class="row q-col-gutter-md">
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="OrgId"
              v-model="form.orgid"
              :error="hasError('orgid')"
              :error-message="fieldError('orgid')"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="OrgName"
              v-model="form.orgname"
              :error="hasError('orgname')"
              :error-message="fieldError('orgname')"
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
import organizationService from '@/services/organization'
import useCrudForm from '@/composables/useCrudForm'

export default defineComponent({
  setup() {
    const { form, loading, hasError, fieldError, onSubmit } = useCrudForm(
      organizationService,
      {
        listRoute: 'organization',
        initialForm: {
          orgid: '',
          orgname: ''
        }
      }
    )

    return {
      form,
      loading,
      hasError,
      fieldError,
      onSubmit
    }
  }
})
</script>

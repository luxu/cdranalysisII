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
              option-label="name"
              option-value="id"
              emit-value
              map-options
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input filled label="SessionId" v-model="form.sessionid" />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="IMSI (Internacional Mobile Subscriber Identity)"
              v-model="form.imsi"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="SessionCreateTime"
              v-model="form.sessioncreatetime"
              type="datetime-local"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="RealUsage (consumo real)"
              v-model="form.realusage"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="UOM (Unidade de Medida, ex: MB, KB)"
              v-model="form.uom"
            />
          </div>
        </div>
        <div class="col-12 col-sm-6 col-md-3">
          <q-btn label="Submit" type="submit" color="primary" />
        </div>
      </q-form>
    </div>
  </q-page>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default defineComponent({
  setup() {
    const form = ref({
      device: null,
      sessionid: '',
      imsi: '',
      sessioncreatetime: '',
      realusage: '',
      uom: ''
    })

    const deviceOptions = ref([
      { id: 1, name: 'Device 1' },
      { id: 2, name: 'Device 2' }
    ])

    const router = useRouter()
    const route = useRoute()

    const isUpdate = computed(() => route.params.id)

    const handleGetSession = async id => {
      console.log('Fetching session data for id:', id)
      // Fetch the session data by ID and populate the form fields
      // Example:
      // const response = await fetch(`/api/sessions/${id}`);
      // const data = await response.json();
      // form.value = {
      //     device: data.device,
      //     sessionid: data.sessionid,
      //     imsi: data.imsi,
      //     sessioncreatetime: data.sessioncreatetime,
      //     realusage: data.realusage,
      //     uom: data.uom,
      // };
    }

    onMounted(() => {
      if (isUpdate.value) {
        handleGetSession(isUpdate.value)
      }
    })

    const onSubmit = () => {
      if (isUpdate.value) {
        // Update the session
        console.log('Updating session:', form.value)
      } else {
        // Create a new session
        console.log('Creating new session:', form.value)
      }
      router.push({ name: 'session' })
    }

    return {
      form,
      deviceOptions,
      handleGetSession,
      onSubmit
    }
  }
})
</script>

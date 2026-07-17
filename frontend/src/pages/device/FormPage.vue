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
              option-label="name"
              option-value="id"
              emit-value
              map-options
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="ICCID (ID do cartão SIM)"
              v-model="form.iccid"
            />
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
              label="MSISDN (número da linha)"
              v-model="form.msisdn"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input filled label="MEI (ID do aparelho)" v-model="form.mei" />
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
      thing: null,
      iccid: '',
      imsi: '',
      msisdn: '',
      mei: ''
    })

    const thingOptions = ref([
      { id: 1, name: 'Thing 1' },
      { id: 2, name: 'Thing 2' }
    ])

    const router = useRouter()
    const route = useRoute()

    const isUpdate = computed(() => route.params.id)

    const handleGetDevice = async id => {
      console.log('Fetching device data for id:', id)
      // Fetch the device data by ID and populate the form fields
      // Example:
      // const response = await fetch(`/api/devices/${id}`);
      // const data = await response.json();
      // form.value = {
      //     thing: data.thing,
      //     iccid: data.iccid,
      //     imsi: data.imsi,
      //     msisdn: data.msisdn,
      //     mei: data.mei,
      // };
    }

    onMounted(() => {
      if (isUpdate.value) {
        handleGetDevice(isUpdate.value)
      }
    })

    const onSubmit = () => {
      if (isUpdate.value) {
        // Update the device
        console.log('Updating device:', form.value)
      } else {
        // Create a new device
        console.log('Creating new device:', form.value)
      }
      router.push({ name: 'device' })
    }

    return {
      form,
      thingOptions,
      handleGetDevice,
      onSubmit
    }
  }
})
</script>

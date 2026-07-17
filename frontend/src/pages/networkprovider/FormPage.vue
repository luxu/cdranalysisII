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
              option-label="name"
              option-value="id"
              emit-value
              map-options
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="NetworkProviderId"
              v-model="form.networkproviderid"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="NetworkProviderName"
              v-model="form.networkprovidername"
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
      customer: null,
      networkproviderid: '',
      networkprovidername: ''
    })

    const customerOptions = ref([
      { id: 1, name: 'Customer 1' },
      { id: 2, name: 'Customer 2' }
    ])

    const router = useRouter()
    const route = useRoute()

    const isUpdate = computed(() => route.params.id)

    const handleGetNetworkProvider = async id => {
      console.log('Fetching networkprovider data for id:', id)
      // Fetch the networkprovider data by ID and populate the form fields
      // Example:
      // const response = await fetch(`/api/networkproviders/${id}`);
      // const data = await response.json();
      // form.value = {
      //     customer: data.customer,
      //     networkproviderid: data.networkproviderid,
      //     networkprovidername: data.networkprovidername,
      // };
    }

    onMounted(() => {
      if (isUpdate.value) {
        handleGetNetworkProvider(isUpdate.value)
      }
    })

    const onSubmit = () => {
      if (isUpdate.value) {
        // Update the networkprovider
        console.log('Updating networkprovider:', form.value)
      } else {
        // Create a new networkprovider
        console.log('Creating new networkprovider:', form.value)
      }
      router.push({ name: 'networkprovider' })
    }

    return {
      form,
      customerOptions,
      handleGetNetworkProvider,
      onSubmit
    }
  }
})
</script>

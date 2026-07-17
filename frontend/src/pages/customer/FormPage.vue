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
              option-label="name"
              option-value="id"
              emit-value
              map-options
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input filled label="CustomerId" v-model="form.customerid" />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input filled label="CustomerName" v-model="form.customername" />
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
      organization: null,
      customerid: '',
      customername: ''
    })

    const organizationOptions = ref([
      { id: 1, name: 'Organization 1' },
      { id: 2, name: 'Organization 2' }
    ])

    const router = useRouter()
    const route = useRoute()

    const isUpdate = computed(() => route.params.id)

    const handleGetCustomer = async id => {
      console.log('Fetching customer data for id:', id)
      // Fetch the customer data by ID and populate the form fields
      // Example:
      // const response = await fetch(`/api/customers/${id}`);
      // const data = await response.json();
      // form.value = {
      //     organization: data.organization,
      //     customerid: data.customerid,
      //     customername: data.customername,
      // };
    }

    onMounted(() => {
      if (isUpdate.value) {
        handleGetCustomer(isUpdate.value)
      }
    })

    const onSubmit = () => {
      if (isUpdate.value) {
        // Update the customer
        console.log('Updating customer:', form.value)
      } else {
        // Create a new customer
        console.log('Creating new customer:', form.value)
      }
      router.push({ name: 'customer' })
    }

    return {
      form,
      organizationOptions,
      handleGetCustomer,
      onSubmit
    }
  }
})
</script>

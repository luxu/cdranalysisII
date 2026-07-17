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
              option-label="name"
              option-value="id"
              emit-value
              map-options
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input filled label="PricePlanId" v-model="form.priceplanid" />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input
              filled
              label="PricePlanName"
              v-model="form.priceplanname"
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
      priceplanid: '',
      priceplanname: ''
    })

    const customerOptions = ref([
      { id: 1, name: 'Customer 1' },
      { id: 2, name: 'Customer 2' }
    ])

    const router = useRouter()
    const route = useRoute()

    const isUpdate = computed(() => route.params.id)

    const handleGetPricePlan = async id => {
      console.log('Fetching priceplan data for id:', id)
      // Fetch the priceplan data by ID and populate the form fields
      // Example:
      // const response = await fetch(`/api/priceplans/${id}`);
      // const data = await response.json();
      // form.value = {
      //     customer: data.customer,
      //     priceplanid: data.priceplanid,
      //     priceplanname: data.priceplanname,
      // };
    }

    onMounted(() => {
      if (isUpdate.value) {
        handleGetPricePlan(isUpdate.value)
      }
    })

    const onSubmit = () => {
      if (isUpdate.value) {
        // Update the priceplan
        console.log('Updating priceplan:', form.value)
      } else {
        // Create a new priceplan
        console.log('Creating new priceplan:', form.value)
      }
      router.push({ name: 'priceplan' })
    }

    return {
      form,
      customerOptions,
      handleGetPricePlan,
      onSubmit
    }
  }
})
</script>

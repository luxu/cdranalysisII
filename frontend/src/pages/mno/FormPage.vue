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
              option-label="name"
              option-value="id"
              emit-value
              map-options
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input filled label="MNOId" v-model="form.mnoid" />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input filled label="MnoName" v-model="form.mnoname" />
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
      mnoid: '',
      mnoname: ''
    })

    const organizationOptions = ref([
      { id: 1, name: 'Organization 1' },
      { id: 2, name: 'Organization 2' }
    ])

    const router = useRouter()
    const route = useRoute()

    const isUpdate = computed(() => route.params.id)

    const handleGetMno = async id => {
      console.log('Fetching mno data for id:', id)
      // Fetch the mno data by ID and populate the form fields
      // Example:
      // const response = await fetch(`/api/mnos/${id}`);
      // const data = await response.json();
      // form.value = {
      //     organization: data.organization,
      //     mnoid: data.mnoid,
      //     mnoname: data.mnoname,
      // };
    }

    onMounted(() => {
      if (isUpdate.value) {
        handleGetMno(isUpdate.value)
      }
    })

    const onSubmit = () => {
      if (isUpdate.value) {
        // Update the mno
        console.log('Updating mno:', form.value)
      } else {
        // Create a new mno
        console.log('Creating new mno:', form.value)
      }
      router.push({ name: 'mno' })
    }

    return {
      form,
      organizationOptions,
      handleGetMno,
      onSubmit
    }
  }
})
</script>

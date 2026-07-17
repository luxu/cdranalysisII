<template>
  <q-page padding>
    <h1 class="text-h2 text-center">Organization Page</h1>
    <div class="q-pa-md" style="max-width: 900px; margin: auto">
      <q-form class="q-gutter-md" @submit.prevent="onSubmit">
        <div class="row q-col-gutter-md">
          <div class="col-12 col-sm-6 col-md-3">
            <q-input filled label="OrgId" v-model="form.orgid" />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input filled label="OrgName" v-model="form.orgname" />
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
      orgid: '',
      orgname: ''
    })

    const router = useRouter()
    const route = useRoute()

    const isUpdate = computed(() => route.params.id)

    const handleGetOrganization = async id => {
      console.log('Fetching organization data for id:', id)
      // Fetch the organization data by ID and populate the form fields
      // Example:
      // const response = await fetch(`/api/organizations/${id}`);
      // const data = await response.json();
      // form.value = {
      //     orgid: data.orgid,
      //     orgname: data.orgname,
      // };
    }

    onMounted(() => {
      if (isUpdate.value) {
        handleGetOrganization(isUpdate.value)
      }
    })

    const onSubmit = () => {
      if (isUpdate.value) {
        // Update the organization
        console.log('Updating organization:', form.value)
      } else {
        // Create a new organization
        console.log('Creating new organization:', form.value)
      }
      router.push({ name: 'organization' })
    }

    return {
      form,
      handleGetOrganization,
      onSubmit
    }
  }
})
</script>

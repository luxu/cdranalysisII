<template>
  <q-page padding>
    <h1 class="text-h2 text-center">{{ isUpdate ? 'Edit' : 'New' }} Profile</h1>
    <div class="q-pa-md" style="max-width: 900px; margin: auto">
      <q-form class="q-gutter-md" @submit.prevent="onSubmit">
        <div class="row q-col-gutter-md">
          <div class="col-12 col-sm-6 col-md-3">
            <q-input filled label="Name" v-model="form.name" />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input filled label="Email" v-model="form.email" type="email" />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input filled label="Photo" v-model="form.photo" />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input filled label="City" v-model="form.city" />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input filled label="Celular" v-model="form.celular" />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-input filled label="Telephone" v-model="form.telephone" />
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
      name: '',
      email: '',
      photo: '',
      city: '',
      celular: '',
      telephone: ''
    })

    const router = useRouter()
    const route = useRoute()

    const isUpdate = computed(() => !!route.params.id)

    const handleGetGasto = async id => {
      console.log('Fetching gasto data for name:', id)
    }

    onMounted(() => {
      if (isUpdate.value) {
        handleGetGasto(isUpdate.value)
      }
    })

    const listRoute = computed(() => {
      return route.meta?.listRoute || { name: 'profile' }
    })

    const onSubmit = () => {
      if (isUpdate.value) {
        console.log('Updating gasto:', form.value)
      } else {
        console.log('Creating new gasto:', form.value)
      }
      router.push(listRoute.value)
    }

    return {
      form,
      isUpdate,
      handleGetGasto,
      onSubmit
    }
  }
})
</script>

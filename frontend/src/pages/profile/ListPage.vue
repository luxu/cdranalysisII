<template>
  <q-page padding>
    <h1 class="text-h2 text-center">Profile List</h1>
    <q-btn
        color="primary"
        label="Add Profile"
        icon="add"
        :to="{ name: 'form-profile' }"
    />
    <q-table        
        :rows="rows"
        :columns="columns"
        row-key="id"
    >
    <template v-slot:body-cell-actions="props">
          <q-td :props="props" class="q-gutter-x-sm">
            <q-btn
              icon="mdi-pencil-outline"
              color="info"
              dense
              size="sm"
              @click="handlerEdit(props.row)"
            >
              <q-tooltip>
                Edit
              </q-tooltip>
            </q-btn>
            <q-btn
              icon="mdi-delete-outline"
              color="negative"
              dense
              size="sm"
              @click="handlerRemove(props.row)"
            >
              <q-tooltip>
                Delete
              </q-tooltip>
            </q-btn>
          </q-td>
        </template>
    </q-table>
  </q-page>
</template>

<script lang="ts">
    import { defineComponent, ref } from 'vue'
    import { columns } from './table';
    import { useRouter } from 'vue-router';

    export default defineComponent({
        setup() {
            // const rows = ref([])
            const router = useRouter();
            const gasto = ref({
                id: null,
                name: '',
                photo: '',
                city: '',
                celular: '',
                telephone: ''
            });

            const rows = ref([
                { id: 1, name: 'John Doe', photo: 'photo1.jpg', city: 'New York', celular: '1234567890', telephone: '123-456-7890' },
                { id: 2, name: 'Jane Smith', photo: 'photo2.jpg', city: 'Los Angeles', celular: '0987654321', telephone: '098-765-4321' },
            ]);
            
            const handlerEdit = (item: any) => {
                router.push(
                    {
                        name: 'form-profile', 
                        params: { id: item.id } // Pass the name as a parameter to the form page
                    }
                )
            }
            
            return {
                rows,
                columns,
                handlerEdit
            }
        }
    })
</script>

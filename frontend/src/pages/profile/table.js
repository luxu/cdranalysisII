import { ref } from 'vue'

const columns = [
  {
    name: 'id',
    label: 'ID',
    align: 'left',
    field: val => val.id,
    sortable: true
  },
  {
    name: 'name',
    label: 'Name',
    align: 'left',
    field: val => val.name,
    sortable: true
  },
  {
    name: 'photo',
    label: 'Photo',
    align: 'left',
    field: val => val.photo,
    sortable: true
  },
  {
    name: 'city',
    label: 'City',
    align: 'left',
    field: val => val.city,
    sortable: true
  },
  {
    name: 'celular',
    label: 'Celular',
    align: 'left',
    field: val => val.celular,
    sortable: true
  },
  {
    name: 'telephone',
    label: 'Telefone',
    align: 'left',
    field: val => val.telephone || '-',
    sortable: true
  },
  {
    name: 'actions',
    align: 'right',
    label: 'Actions',
    field: 'actions',
    sortable: false
  }
]

const initialPagination = ref({
  page: 1,
  rowsPerPage: 8
})

export { columns, initialPagination }

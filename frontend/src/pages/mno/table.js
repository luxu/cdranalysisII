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
    name: 'mnoid',
    label: 'MNOId',
    align: 'left',
    field: val => val.mnoid,
    sortable: true
  },
  {
    name: 'mnoname',
    label: 'MnoName',
    align: 'left',
    field: val => val.mnoname,
    sortable: true
  },
  {
    name: 'organization',
    label: 'Organization',
    align: 'left',
    field: val => val.organization_name || val.organization,
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

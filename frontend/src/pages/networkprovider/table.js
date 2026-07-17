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
    name: 'networkproviderid',
    label: 'NetworkProviderId',
    align: 'left',
    field: val => val.networkproviderid,
    sortable: true
  },
  {
    name: 'networkprovidername',
    label: 'NetworkProviderName',
    align: 'left',
    field: val => val.networkprovidername,
    sortable: true
  },
  {
    name: 'customer',
    label: 'Customer',
    align: 'left',
    field: val => val.customer_name || val.customer,
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

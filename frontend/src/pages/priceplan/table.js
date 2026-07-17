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
    name: 'priceplanid',
    label: 'PricePlanId',
    align: 'left',
    field: val => val.priceplanid,
    sortable: true
  },
  {
    name: 'priceplanname',
    label: 'PricePlanName',
    align: 'left',
    field: val => val.priceplanname,
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

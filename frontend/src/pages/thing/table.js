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
    name: 'thingsgroupid',
    label: 'ThingsGroupId',
    align: 'left',
    field: val => val.thingsgroupid,
    sortable: true
  },
  {
    name: 'thingsgroupname',
    label: 'ThingsGroupName',
    align: 'left',
    field: val => val.thingsgroupname,
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

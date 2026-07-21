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
    name: 'thing',
    label: 'Thing',
    align: 'left',
    field: val => val.thing_name || val.thing,
    sortable: true
  },
  {
    name: 'iccid',
    label: 'ICCID',
    align: 'left',
    field: val => val.iccid || '-',
    sortable: true
  },
  {
    name: 'imsi',
    label: 'IMSI',
    align: 'left',
    field: val => val.imsi,
    sortable: true
  },
  {
    name: 'msisdn',
    label: 'MSISDN',
    align: 'left',
    field: val => val.msisdn,
    sortable: true
  },
  {
    name: 'imei',
    label: 'IMEI',
    align: 'left',
    field: val => val.mei,
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

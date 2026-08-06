import { ref } from 'vue'

const sessionColumns = [
  {
    name: 'sessionid',
    label: 'Session ID',
    align: 'left',
    field: val => val.sessionid,
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
    name: 'sessioncreatetime',
    label: 'Data',
    align: 'left',
    field: val => val.sessioncreatetime,
    sortable: true
  },
  {
    name: 'realusage',
    label: 'Uso',
    align: 'right',
    field: val => val.realusage,
    sortable: true
  },
  {
    name: 'uom',
    label: 'UOM',
    align: 'left',
    field: val => val.uom,
    sortable: true
  }
]

const sessionPagination = ref({
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0,
  sortBy: '',
  descending: false
})

export { sessionColumns, sessionPagination }

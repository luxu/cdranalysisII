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
    name: 'device',
    label: 'Device',
    align: 'left',
    field: val => val.device_name || val.device,
    sortable: true
  },
  {
    name: 'sessionid',
    label: 'SessionId',
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
    label: 'SessionCreateTime',
    align: 'left',
    field: val => val.sessioncreatetime,
    sortable: true
  },
  {
    name: 'realusage',
    label: 'RealUsage',
    align: 'left',
    field: val => val.realusage,
    sortable: true
  },
  {
    name: 'uom',
    label: 'UOM',
    align: 'left',
    field: val => val.uom,
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

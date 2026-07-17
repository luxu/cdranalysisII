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
    name: 'orgid',
    label: 'OrgId',
    align: 'left',
    field: val => val.orgid,
    sortable: true
  },
  {
    name: 'orgname',
    label: 'OrgName',
    align: 'left',
    field: val => val.orgname,
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

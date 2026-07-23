const columns = [
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
    name: 'msisdn',
    label: 'MSISDN',
    align: 'left',
    field: val => val.msisdn,
    sortable: true
  },
  {
    name: 'thing_name',
    label: 'Thing',
    align: 'left',
    field: val => val.thing_name,
    sortable: true
  },
  {
    name: 'sessioncreatetime',
    label: 'Data Criação',
    align: 'left',
    field: val => val.sessioncreatetime,
    sortable: true
  },
  {
    name: 'realusage',
    label: 'Real Usage',
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
  },
  {
    name: 'status',
    label: 'Ativo',
    align: 'center',
    field: val => val.status,
    sortable: true
  }
]

export { columns }

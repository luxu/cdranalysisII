const columns = [
  {
    name: 'sessionid',
    label: 'Session ID',
    align: 'left',
    field: val => val.sessionid,
    sortable: true
  },
  {
    name: 'iccid',
    label: 'ICCID',
    align: 'left',
    field: val => val.iccid,
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
    format: val => {
      if (!val) return ''
      const d = new Date(val)
      return d.toLocaleDateString('pt-BR')
    },
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
  }
]

export { columns }

const columns = [
  {
    name: 'name',
    label: 'Nome',
    align: 'left',
    field: val => val.name,
    sortable: true
  },
  {
    name: 'user_email',
    label: 'Email',
    align: 'left',
    field: val => val.user_email,
    sortable: true
  },
  {
    name: 'celular',
    label: 'Celular',
    align: 'left',
    field: val => val.celular || '-',
    sortable: true
  },
  {
    name: 'thing_name',
    label: 'Thing',
    align: 'left',
    field: val => val.thing_name || '-',
    sortable: true
  },
  {
    name: 'status',
    label: 'Ativo',
    align: 'center',
    field: val => val.status,
    format: val => (val ? 'Sim' : 'Não'),
    sortable: true
  },
  {
    name: 'actions',
    align: 'right',
    label: 'Ações',
    field: 'actions',
    sortable: false
  }
]

export { columns }

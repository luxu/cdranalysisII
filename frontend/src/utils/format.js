export function formatNumber(value) {
  if (value === null || value === undefined || value === '') return '0'
  const num = typeof value === 'string' ? parseFloat(value) : Number(value)
  if (isNaN(num)) return String(value)
  return Math.round(num).toLocaleString('pt-BR')
}

function _formatIsoDate(iso) {
  if (!iso) return ''
  const parts = iso.split('-')
  if (parts.length !== 3) return iso
  return `${parts[2]}/${parts[1]}`
}

export function formatPeriod(start, end) {
  const s = _formatIsoDate(start)
  const e = _formatIsoDate(end)
  if (!s && !e) return ''
  if (s && e) {
    if (s === e) return s
    return `${s} a ${e}`
  }
  if (s) return `a partir de ${s}`
  return `até ${e}`
}

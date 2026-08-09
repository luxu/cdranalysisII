export function formatNumber(value) {
  if (value === null || value === undefined || value === '') return '0'
  const num = typeof value === 'string' ? parseFloat(value) : Number(value)
  if (isNaN(num)) return String(value)
  return Math.round(num).toLocaleString('pt-BR')
}

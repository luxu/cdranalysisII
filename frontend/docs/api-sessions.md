# API de Sessões

Serviço de consulta e análise de sessões de uso de dados.

**Arquivo:** `src/services/session.js`

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| CRUD | `/api/sessions/` | Operações padrão (listar, buscar, criar, atualizar, excluir) |
| `dateRange()` | `/api/sessions/date_range/` | Intervalo de datas disponível |
| `summaryByThing()` | `/api/sessions/summary_by_thing/` | Resumo de uso por dispositivo |
| `topDevices()` | `/api/sessions/top_devices/` | Ranking de consumo |
| `usageByMonth()` | `/api/sessions/usage_by_month/` | Consumo mensal |
| `countByUom()` | `/api/sessions/count_by_uom/` | Contagem por unidade de medida |

## Detalhamento

### `dateRange()`

Retorna as datas mínima e máxima das sessões cadastradas. Útil para popular selects de filtro de período.

**Retorno:** `{ min: "2024-01-15", max: "2025-10-21" }`

### `summaryByThing(params)`

Agrupa sessões por "thing" (dispositivo) e retorna métricas consolidadas.

**Parâmetros:**
- `start_date` — Data início (opcional)
- `end_date` — Data fim (opcional)

### `topDevices(params)`

Lista os dispositivos com maior consumo de dados, ordenados por uso.

**Parâmetros:**
- `start_date` — Data início (opcional)
- `end_date` — Data fim (opcional)

### `usageByMonth(params)`

Retorna o consumo total agrupado por mês. Ideal para gráficos de tendência.

**Parâmetros:**
- `start_date` — Data início (opcional)
- `end_date` — Data fim (opcional)

### `countByUom(params)`

Conta sessões agrupadas por unidade de medida (MB, GB, etc).

**Parâmetros:**
- `start_date` — Data início (opcional)
- `end_date` — Data fim (opcional)

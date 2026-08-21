# ROADMAP — CDR Analysis

Guia para entender o projeto de ponta a ponta.

## Visão Geral

Plataforma de análise de CDR (Call Detail Record) para IoT/SIM cards. Duas apps independentes:

```
backend/   → Django 6 + DRF + SQLite (dev)
frontend/  → Vue 3 + Quasar v2 (Vite)
```

Não há ferramentas compartilhadas entre elas. Cada uma tem seu próprio `package.json` / `pyproject.toml`.

---

## Modelo de Dados

```
Organization
  └── Customer
       ├── Thing (grupo de dispositivos)
       │    └── Device (SIM chip: iccid, imsi, imei)
       │         └── Session (registro de uso: sessionid, data, bytes, uom)
       ├── NetworkProvider
       └── PricePlan
  └── Mno (operadora de rede)
```

Todos os modelos usam UUID como PK (via `core.Base`).

---

## Backend

### Estrutura

```
backend/
├── kernel/          # Config do Django (settings, urls, middleware)
├── core/            # Modelo abstrato Base (created_at, modified_at, status)
├── cdr/             # Models de negócio (Organization, Customer, Thing, Device, Session...)
├── user/            # User customizado (auth por e-mail) + Profile
├── api/             # ViewSets + Serializers (os que o router usa)
│   ├── urls.py      # Router com todos os endpoints
│   ├── views.py     # ViewSets ativos
│   ├── serializers.py
│   └── services.py  # Importação de CDR via pandas
└── tools/           # Scripts de carga de dados (load_cdr_v2/v3/v4)
```

**Atenção:** Existem ViewSets duplicados em `cdr/views.py` e `user/views.py`, mas os que o router usa são os de `api/views.py`.

### Comandos

```bash
cd backend
task runserver      # localhost:8000
task makemigrations
task migrate
task loadfixtures   # migra + carrega fixtures
task lint           # ruff check
task pytest         # uv run pytest -vv
```

### API REST

Todas as rotas ficam em `/api/`. Exemplos de chamada:

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@admin.com", "password": "123mudar"}'

# Listar sessões (com token)
curl http://localhost:8000/api/sessions/ \
  -H "Authorization: Token <seu_token>"

# Buscar por Thing
curl "http://localhost:8000/api/sessions/?search=VERACRUZ" \
  -H "Authorization: Token <seu_token>"

# Filtrar por data
curl "http://localhost:8000/api/sessions/?start_date=2025-01-01&end_date=2025-12-31" \
  -H "Authorization: Token <seu_token>"

# Top 10 dispositivos
curl http://localhost:8000/api/sessions/top_devices/ \
  -H "Authorization: Token <seu_token>"

# Uso por mês
curl http://localhost:8000/api/sessions/usage_by_month/ \
  -H "Authorization: Token <seu_token>"
```

### Endpoints customizados de Session

| Endpoint | O que retorna |
|----------|---------------|
| `GET /sessions/date_range/` | Data mínima e máxima das sessões |
| `GET /sessions/summary_by_thing/` | Resumo por Thing (qtd dispositivos, uso total) |
| `GET /sessions/top_devices/` | Top 10 dispositivos por consumo |
| `GET /sessions/usage_by_month/` | Consumo mensal (para gráficos) |
| `GET /sessions/count_by_uom/` | Contagem por unidade de medida |
| `POST /sessions/import-cdr/` | Importar CDR de arquivo Excel/CSV (admin only) |

### Autenticação

- **Login:** POST `/api/auth/login/` com email + senha → retorna `{token, user}`
- **Requests:** Header `Authorization: Token <token>`
- **Permissão padrão:** `IsAuthenticated` (todas as rotas requerem login)
- **Rotas admin:** Verificam `is_staff` ou grupo "Administrador"/"Manager"

### Isolamento de Dados (Owner Filter)

O `OwnerFilteredMixin` em `api/views.py` filtra automaticamente:
- **Admin/Manager:** vê tudo
- **Usuário comum:** vê apenas dados do seu `thing` (via `Profile.thing`)

---

## Frontend

### Estrutura

```
frontend/src/
├── boot/
│   ├── axios.js     # Instância axios (baseURL: /api) + interceptor de erros
│   └── auth.js      # Token no header + validação no boot + route guard
├── router/
│   └── routes.js    # Rotas: /login, / (user), /admin (staff)
├── services/        # Camada de API (factory CRUD genérico)
│   ├── crud.js      # Factory: list, get, create, update, remove
│   ├── endpoints.js # Mapa de endpoints
│   └── session.js   # Extende CRUD com endpoints customizados
├── composables/     # Lógica reativa reusável
│   ├── useAuth.js         # Login/logout, token, role, isAutenticated
│   ├── useCrudList.js     # Lista paginada + delete com confirmação
│   ├── useCrudForm.js     # Create/update com erros DRF por campo
│   ├── useOptions.js      # Popula selects de FK
│   └── useDashboardFilter.js  # Filtros compartilhados do dashboard
├── layouts/
│   ├── MainLayout.vue     # Layout do usuário (sidebar com filtros)
│   └── AdminLayout.vue    # Layout do admin (sidebar admin)
├── components/
│   ├── AppSidebar.vue     # Sidebar do usuário
│   ├── AdminSidebar.vue   # Sidebar do admin
│   └── MetricCard.vue     # Card de métrica do dashboard
└── pages/
    ├── LoginPage.vue      # Tela de login
    ├── PanelPage.vue      # Roteador: AdminPanel ou UserPanel
    ├── AdminPanel.vue     # Dashboard admin (gráficos SVG)
    ├── UserPanel.vue      # Dashboard do usuário
    ├── AdminPage.vue      # Painel admin (/admin)
    ├── LoadPage.vue       # Importação de CDR
    ├── device/            # CRUD de dispositivos
    ├── thing/             # CRUD de Things
    ├── profile/           # CRUD de perfis/usuários
    └── session/           # Lista de sessões com filtros
```

### Comandos

```bash
cd frontend
pnpm install     # Instala deps + roda quasar prepare
pnpm dev         # localhost:9000 com HMR
pnpm build       # Build de produção → dist/spa/
pnpm lint        # oxfmt + oxlint --fix
pnpm lint:check  # Verificação sem escrita
```

### Fluxo de Autenticação

```
1. LoginPage.vue
   └── authService.login(email, password)
        └── POST /api/auth/login/
             └── Retorna {token, user: {id, email, is_staff, groups}}

2. useAuth.js
   └── Salva token + user no localStorage

3. boot/auth.js (request interceptor)
   └── Lê localStorage → Header: Authorization: Token <token>

4. boot/auth.js (response interceptor)
   └── 401 → limpa localStorage → redireciona /login

5. boot/auth.js (route guard)
   └── beforeEach: sem token → /login
       requiresStaff: só admin/manager
```

### Criando uma nova tela CRUD

**Exemplo: criar tela de Things**

1. **Service** (`src/services/thing.js`):
```js
import createCrudService from './crud'
import endpoints from './endpoints'
export default createCrudService(endpoints.thing)
```

2. **Table columns** (`src/pages/thing/table.js`):
```js
const columns = [
  { name: 'thingsgroupname', label: 'Nome', field: 'thingsgroupname', sortable: true },
  { name: 'customer', label: 'Cliente', field: val => val.customer_name, sortable: true },
]
export { columns }
```

3. **ListPage** (`src/pages/thing/ListPage.vue`):
```vue
<template>
  <q-page padding>
    <q-table :rows="rows" :columns="columns" row-key="id"
      @request="onRequest" v-model:pagination="pagination" :loading="loading">
      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <q-btn flat dense icon="edit" :to="`/admin/things/${props.row.id}/edit`" />
          <q-btn flat dense icon="delete" color="negative"
            @click="confirmRemove(props.row, props.row.thingsgroupname)" />
        </q-td>
      </template>
    </q-table>
  </q-page>
</template>

<script setup>
import { columns } from './table'
import thingService from '@/services/thing'
import useCrudList from '@/composables/useCrudList'

const { rows, loading, pagination, onRequest, confirmRemove } =
  useCrudList(thingService, { entityLabel: 'Thing' })
</script>
```

4. **Rota** (`src/router/routes.js`):
```js
{ path: 'things', component: () => import('pages/thing/ListPage.vue') },
{ path: 'things/:id/edit', component: () => import('pages/thing/FormPage.vue') },
```

5. **Endpoint** (`src/services/endpoints.js`):
```js
thing: '/things/',
```

### Proxy (Dev Server)

O `quasar.config.js` tem:
```js
devServer: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    }
  }
}
```

Frontend (porta 9000) chama `/api/...` → proxy redireciona para Backend (porta 8000).

---

## Importação de CDR

1. Admin acessa `/admin/xlsx` (LoadPage.vue)
2. Seleciona arquivo Excel/CSV
3. Preview client-side via SheetJS (`xlsx`)
4. Clica "Importar para o Banco"
5. Frontend envia `POST /api/sessions/import-cdr/` com multipart
6. Backend lê com pandas, popula Organization → Customer → Thing → Device → Session
7. Retorna estatísticas (qtd registros, erros)

---

## Dicas para Contribuidores

### Backend

- **Não modifique `cdr/views.py`** — os ViewSets ativos estão em `api/views.py`
- **Serializers:** `api/serializers.py` (não `cdr/serializers.py`)
- **Migrações:** sempre rode `task makemigrations && task migrate` após alterar models
- **Testes:** rode `task pytest` (usa pytest com fixtures em `conftest.py`)

### Frontend

- **Lint:** rode `pnpm lint` antes de commitar (oxfmt + oxlint juntos)
- **Não existe ESLint/Prettier** — usa oxfmt e oxlint
- **Composables são singletons** — `useAuth` e `useDashboardFilter` usam state de módulo
- **Nenhum Pinia/Vuex** — estado global via composables com `ref()` no nível de módulo

### Padronização de commits

```
feat(scope): adicionar funcionalidade
fix(scope): corrigir bug
refactor(scope): reestruturar código
docs: documentação
chore: manutenção
```

Exemplos:
```
feat(api): adiciona filtro search na listagem de sessoes
fix(ui): preserva filtros ao paginar na lista de sessoes
refactor(api): remove campos status e imsi dos serializers
```

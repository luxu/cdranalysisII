# Sistema de Roles (Grupos)

## Grupos definidos

| Grupo         | `role` (useAuth) | `canAccessAdmin` | Login redirect | Acessa `/admin` |
| ------------- | ---------------- | ---------------- | -------------- | --------------- |
| Administrador | `admin`          | `true`           | `/admin`       | Sim             |
| Manager       | `manager`        | `true`           | `/admin`       | Sim             |
| Usuario       | `user`           | `false`          | `/`            | Não (bloqueado) |
| sem grupo     | `null`           | `false`          | `/`            | Não (bloqueado) |

## Onde cada role é verificada

### Login (`user/views.py:29`)

Retorna `groups: list(user.groups.values_list('name', flat=True))` no payload da resposta.

### Composável `useAuth.js`

- `role` — `'admin'` / `'manager'` / `'user'` / `null`
- `canAccessAdmin` — `true` apenas para Administrador e Manager

### Route guard (`boot/auth.js`)

- Requer autenticação global (redireciona para `/login`)
- Usuário já autenticado em `/login` → redireciona conforme grupo
- `requiresStaff` → permite apenas Administrador e Manager
- `requiresAdmin` → permite apenas Administrador (definido, mas nenhuma rota usa)

### Login redirect (`LoginPage.vue:78-83`)

Admin/Manager → `/admin`; demais → `/`

### Atribuição de grupos

Fixture `backend/user/fixtures/01_groups.json` com 3 grupos carregados via `task setupdb`.

## Histórico de correções

Todos os bugs identificados na análise inicial foram corrigidos:

### 1. Herança de `meta` em rotas filhas

**Corrigido em:** `feat(auth): implement role-based routing and sidebar logout`

O guard usava `to.meta?.requiresStaff` que não herda meta de rotas pai. Substituído por `to.matched.some(r => r.meta?.requiresStaff)` em `boot/auth.js`.

### 2. Link Admin visível para Usuario

**Corrigido em:** `feat(auth): implement role-based routing and sidebar logout`

Adicionado `v-if="canAccessAdmin"` ao `RouterLink` do Admin em `AppSidebar.vue`.

### 3. Labels do AdminPage

**Corrigido em:** `feat(profile): add profile CRUD with auto-create user`

Card renomeado de "Grupos User" para "Clientes" com descrição atualizada em `AdminPage.vue`.

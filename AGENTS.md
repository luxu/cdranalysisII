# AGENTS.md

## Estrutura

Duas apps independentes, sem ferramentas compartilhadas entre elas:

- `backend/` — Django 6, Python 3.13+, SQLite (dev), `uv` + `taskipy` como task runner
- `frontend/` — Vue 3, Quasar v2 (Vite), `oxlint` + `oxfmt` (não ESLint/Prettier)

## Comandos do backend (a partir de `backend/`)

Todas as tarefas usam `uv run` por baixo dos panos. Invocadas via taskipy:

```
task runserver        # Servidor de desenvolvimento Django (porta 8000)
task makemigrations   # Gerar migrações
task migrate          # Aplicar migrações
task loadfixtures     # Migra + carrega fixtures
task dumpfixtures     # Exporta fixtures dos models
task setupdb          # makemigrations + migrate + loadfixtures
task lint             # ruff check
task lint_fix         # ruff check --fix
task pytest           # uv run pytest -vv
task shell_plus       # shell django-extensions
```

## Comandos do frontend (a partir de `frontend/`)

```
pnpm install          # Instala deps + roda `quasar prepare --silent` via postinstall
pnpm dev              # Servidor de desenvolvimento Vite com HMR
pnpm build            # Build de produção → dist/spa/
pnpm lint             # oxfmt + oxlint --fix  (formatação + correção de lint em um passo)
pnpm lint:check       # oxfmt --check + oxlint  (apenas verificação, sem escrita)
```

Configuração de lint: `.oxlintrc.json` (plugins: vue, import, eslint, promise, unicorn), `.oxfmtrc.json` (aspas simples, sem ponto e vírgula, 80 caracteres de largura).

## REST API (DRF)

A API REST está exposta em `/api/` via Django REST Framework com `DefaultRouter`.

### Endpoints

| Endpoint | Model | FK(s) |
|----------|-------|-------|
| `/api/organizations/` | Organization | — |
| `/api/customers/` | Customer | organization |
| `/api/mnos/` | Mno | organization |
| `/api/networkproviders/` | NetworkProvider | customer |
| `/api/priceplans/` | PricePlan | customer |
| `/api/things/` | Thing | customer |
| `/api/devices/` | Device | thing |
| `/api/sessions/` | Session | device |
| `/api/profiles/` | Profile | user |

Cada endpoint suporta: GET (list), POST (create), GET/{id}/ (retrieve), PUT/PATCH (update), DELETE (destroy).

### Configuração

- **Autenticação:** Session + Token (`rest_framework.authentication`)
- **Permissão:** `IsAuthenticated` (padrão global)
- **Paginação:** 50 itens/página (`PageNumberPagination`)
- **CORS:** `CORS_ALLOW_ALL_ORIGINS = True` (dev)
- **Serializers:** `cdr/serializers.py`, `user/serializers.py` (ModelSerializer com UUID PKs)
- **ViewSets:** `cdr/views.py`, `user/views.py` (ModelViewSet com select_related)

### Frontend → Backend

O proxy do devServer já está configurado no `quasar.config.js`:
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

Camada de API do frontend:

- `src/boot/axios.js` — instância `api` do axios com `baseURL: '/api'` e interceptor que normaliza erros em `error.friendlyMessage`
- `src/services/` — factory CRUD genérico (`crud.js`: `list/get/create/update/remove`) + um módulo por entidade; caminhos centralizados em `endpoints.js`
- `src/composables/` — `useCrudList` (lista paginada DRF + delete com confirmação), `useCrudForm` (create/update + erros de validação DRF por campo), `useOptions` (popula selects de FK)

## Notas de arquitetura

- **Modelo de User customizado** — `user.User` usa autenticação por e-mail, não por nome de usuário. Definido via `AUTH_USER_MODEL = 'user.User'`.
- **LoginRequiredMiddleware está ativo** — todas as views do Django requerem autenticação por padrão.
- **Chaves primárias UUID** — todos os modelos CDR usam `UUIDField` como PKs via o modelo abstrato `core.Base`.
- **Ingestão de dados via scripts** — `tools/load_cdr.py` (v1) e `tools/load_cdr_v2.py` (otimizado) leem arquivos Excel no servidor via pandas/openpyxl e populam o ORM diretamente. Não exposto via API.
- **Localização** — `pt-br`, timezone `America/Sao_Paulo`. Textos da UI e muitos comentários estão em português brasileiro.

## Ambiente de desenvolvimento

- O `.env` do backend fica em `backend/.env` (usa `python-decouple`). Contém `BACKEND_SECRET_KEY`, `BACKEND_DEBUG`, `BACKEND_ALLOWED_HOSTS`.
- SQLite é o banco de desenvolvimento padrão. A configuração do Postgres está comentada no `settings.py`; Docker Compose em `backend/docker/docker-compose.yml` fornece Postgres 17.6.
- `dist/spa/` (assets do frontend buildados) é commitado no git.
- `processador.py` é um arquivo esqueleto — não funcional, ignorar.

## Testes

Nenhum arquivo de teste existe ainda. `task pytest` executa `uv run pytest -vv` mas não há testes para rodar.

## Cuidados

- `pnpm lint` do frontend roda o formatador + linter juntos — não existe comando separado para formatação.
- Requisito de engine Node no `package.json`: `>= 26 || ^24 || ^22.12`.

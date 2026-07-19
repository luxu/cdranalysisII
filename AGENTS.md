# AGENTS.md

## Estrutura

Duas apps independentes, sem ferramentas compartilhadas entre elas:

- `backend/` — Django 6, Python 3.13+, SQLite (dev), `uv` + `taskipy` como task runner
- `frontend/` — Vue 3, Quasar v2 (Vite), `oxlint` + `oxfmt` (não ESLint/Prettier)

## Comandos do backend (a partir de `backend/`)

Todas as tarefas usam `uv run` por baixo dos panos. Invocadas via taskipy:

```
task runserver        # Servidor de desenvolvimento Django (porta 8000)
task 8004             # Servidor de desenvolvimento na porta 8004
task makemigrations   # Gerar migrações
task migrate          # Aplicar migrações
task reset            # Reset completo do DB: apaga migrações + db.sqlite3, re-migra, cria superusuário
task cdr              # Carrega dados CDR de files/cdr.xlsx via tools/load_cdr.py
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

## Notas de arquitetura

- **Não existe REST API ainda.** `kernel/urls.py` só expõe `/admin/`. DRF e CORS estão comentados nas configurações. As páginas do frontend usam dados mock hardcoded.
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
- `task reset` é destrutivo — apaga `db.sqlite3` e todos os arquivos de migração antes de recriar do zero.
- Requisito de engine Node no `package.json`: `>= 26 || ^24 || ^22.12`.

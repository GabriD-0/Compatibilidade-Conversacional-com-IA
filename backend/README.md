# Backend (Flask)

API REST com autenticação (cadastro, login, refresh JWT, recuperação de senha) e PostgreSQL. O ambiente pode usar conexão **direta** ao banco ou **túnel SSH** (útil quando o Postgres só é acessível pelo servidor remoto).

## Pré-requisitos

- Python 3.11+ recomendado
- PostgreSQL acessível (local, na rede ou via túnel SSH)
- Variáveis de ambiente para banco e segredos (veja abaixo)

## Configuração rápida

Na raiz do repositório, entre na pasta do backend:

```bash
cd backend
```

1. Crie e ative um ambiente virtual (recomendado):

   ```bash
   python -m venv .venv
   ```

   - **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
   - **Linux/macOS:** `source .venv/bin/activate`

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Defina `FLASK_APP` e aplique as migrações (cria/atualiza tabelas no banco configurado):

   **Windows (cmd):**

   ```cmd
   set FLASK_APP=run:app
   flask db upgrade
   ```

   **Windows (PowerShell):**

   ```powershell
   $env:FLASK_APP = "run:app"
   flask db upgrade
   ```

   **Linux/macOS:**

   ```bash
   export FLASK_APP=run:app
   flask db upgrade
   ```

   Na **primeira vez** no repositório, se a pasta `migrations` ainda não existir, use antes `flask db init` (já commitada neste projeto em geral não é necessário).

4. Suba o servidor de desenvolvimento:

   ```bash
   python run.py
   ```

   Por padrão a API fica em `http://127.0.0.1:5000`.

- **Saúde:** `GET http://127.0.0.1:5000/health`
- **Auth (prefixo):** `http://127.0.0.1:5000/api/auth/` (`register`, `login`, `refresh`, `forgot-password`, `reset-password`)

## Variáveis de ambiente importantes

Crie um arquivo `.env` na pasta `backend` (o `python-dotenv` carrega automaticamente) ou exporte no shell.

| Variável | Descrição |
|----------|-----------|
| `FLASK_ENV` | `development` (padrão em `run.py`), `production` ou `prod` (equivale a produção) |
| `SECRET_KEY` | Chave secreta da aplicação (obrigatória em produção) |
| `JWT_SECRET_KEY` | Chave dos JWT (opcional; usa `SECRET_KEY` se omitida) |
| `DB_USER`, `DB_PASSWORD`, `DB_NAME` | Credenciais PostgreSQL |
| `DB_HOST`, `DB_PORT` | Host e porta do Postgres (ex.: `127.0.0.1` e `5432`) |
| `CORS_ORIGINS` | Origens permitidas, separadas por vírgula (ex.: `http://localhost:5173`) |

### Túnel SSH (opcional)

| Variável | Descrição |
|----------|-----------|
| `DB_USE_SSH_TUNNEL` | `true` / `1` para ativar |
| `SSH_HOST`, `SSH_PORT`, `SSH_USERNAME` | Servidor e usuário SSH |
| `SSH_KEY_PATH` | Caminho da chave privada (preferível) **ou** |
| `SSH_PASSWORD` | Senha SSH (menos seguro) |
| `SSH_REMOTE_BIND_ADDRESS` | Onde o Postgres escuta no servidor (geralmente `127.0.0.1`) |
| `SSH_REMOTE_BIND_PORT` | Porta do Postgres no servidor (geralmente `5432`) |
| `SSH_LOCAL_BIND_PORT` | Porta local; `0` deixa o SO escolher |

Com o túnel ativo, a URI interna aponta para `127.0.0.1` na porta local encaminhada; `DB_HOST`/`DB_PORT` da conexão direta não são usados para o Postgres nesse modo.

### E-mail (recuperação de senha)

Configure `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER` e `PASSWORD_RESET_FRONTEND_URL`. Em desenvolvimento, sem SMTP, o link pode ser registrado no log se `LOG_RESET_TOKEN_IN_DEV=true`.

## Produção

Use `FLASK_ENV=production` (ou `prod`), chaves fortes, SMTP configurado e `flask db upgrade` no deploy. Para servir com um WSGI (ex.: Gunicorn), importe `app` de `run:app` conforme a documentação do servidor escolhido.
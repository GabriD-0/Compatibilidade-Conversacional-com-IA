# Backend

API REST.

## Pré-requisitos

- Python 3.11+ recomendado
- Variáveis de ambiente para banco de dados

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

   > **Nota sobre a Primeira Execução:**
   > Se for a sua primeira vez rodando o projeto ou se a pasta `migrations` não existir, você precisará inicializar as migrações e criar o histórico inicial antes do comando de `upgrade` e criação do banco:
   > 
   > 1. `flask db init` (Gera a pasta de migrações)
   > 2. `flask db migrate -m "Migração inicial"` (Lê os seus modelos como `Login` e cria o histórico das tabelas)
   > 3. `flask db upgrade` (Aplica as mudanças de fato no seu Banco PostgreSQL)

4. Suba o servidor de desenvolvimento:

   ```bash
   python run.py
   ```

   Por padrão a API fica em `http://127.0.0.1:5000`.

## Variáveis de ambiente importantes

Crie um arquivo `.env` na pasta `backend` ou exporte no shell.
# Auth Server Python

Authorization Server OAuth 2.0 (FastAPI) com fluxo `authorization_code` + PKCE (`S256`) e emissão de JWT assinados em `RS256`.

## Resumo rapido

- API em FastAPI com endpoints: Clients, users, scopes, claims, `authorize`, `token` e JWKS.
- Persistência local(por hora) em SQLite (`app/auth.db`).
- Chaves RSA (`private.pem` / `public.pem`) geradas automaticamente no startup (se não existirem).
- Login web por cliente em `/{client_name}/login`.

## Requisitos

- Python 3.13 (ou 3.11+ com ajuste de dependências)
- `pip`
- `requirements.txt`

Instalação recomendada:

```bash
python -m venv .venv
. .venv/Scripts/activate(or .venv/bin/activate on linux)
pip install -r requirements.txt
```

## Envs

Obrigatorias:

- `ADMIN_TOKEN`: token de administração para rotas protegidas por header `admin-token`.
- `SECRET_KEY`: secret da sessão (`SessionMiddleware`).

Recomendadas:

- `SESSION_EXPIRE`: expiração da sessão em minutos (padrão: `30`).
- `APP_ENV`: `development` (padrão), `dev`, `prod`, `test` etc.
- `ISSUER`: valor de `iss` no JWT.
- `PRIVATE_KEY_PATH`: caminho da chave privada (padrão: `private.pem`).
- `PUBLIC_KEY_PATH`: caminho da chave publica (padrão: `public.pem`).

Exemplo (PowerShell):

```powershell
$env:ADMIN_TOKEN = "admin"
$env:SECRET_KEY = "change-me"
$env:SESSION_EXPIRE = "30"
$env:APP_ENV = "dev"
$env:ISSUER = "http://localhost:8000"
```

Exemplo (Linux):

```bash
export ADMIN_TOKEN = "admin"
export SECRET_KEY = "change-me"
export SESSION_EXPIRE = "30"
export APP_ENV = "dev"
export ISSUER = "http://localhost:8000"
```

## Como rodar

Importante: É recomendado executar a aplicação dentro da pasta `app`(caso use as chaves pré-geradas), para que as chaves
sejam geradas dentro do escopo da mesma.

```
cd app
uvicorn main:application --reload
```

Docs locais:

- Swagger: `http://localhost:8000/docs`
- OpenAPI: `http://localhost:8000/openapi.json`
- JWKS: `http://localhost:8000/api/.well-known/jwks.json`

## Endpoints principais

- `GET /api/authorize`
- `POST /api/token`
- `GET /api/.well-known/jwks.json`
- `GET/POST /{client_name}/login`
- `GET/POST/DELETE /api/clients` (admin)
- `GET/POST/DELETE /api/{client_name}/users`
- `GET/POST/DELETE /api/scopes`
- `GET/POST/DELETE /api/claims` (admin-token ou token)

## Como rodar testes

Na raiz do projeto:

```powershell
.\.venv\Scripts\pytest -q
```

## Exemplo de integração com oidcdebugger.com(para testescurl --location 'http://localhost:8000/api/clients' \
--header 'admin-token: admin' \
--header 'Content-Type: application/json' \
--data '{
    "redirect_uri": "https://oidcdebugger.com/debug",
    "scopes": ["read", "write", "openid"],
    "grant_types": ["authorization_code", "refresh_token"],
    "client_type": "public",
    "response_type": "code",
    "token_exp": 5,
    "refresh_token_exp": 10,
    "code_exp": 3,
    "name": "demo"
}')

### 1) Criar client OAuth

```bash
curl --location 'http://localhost:8000/api/clients' \
--header 'admin-token: {ADMIN_TOKEN_ENV}' \
--header 'Content-Type: application/json' \
--data '{
    "redirect_uri": "https://oidcdebugger.com/debug",
    "scopes": ["read", "write", "openid"],
    "grant_types": ["authorization_code", "refresh_token"],
    "client_type": "public",
    "response_type": "code",
    "token_exp": 5,
    "refresh_token_exp": 10,
    "code_exp": 3,
    "name": "demo"
}'
```

Guarde o `client_id` retornado.

### 2) Criar usuario para esse client

```bash
curl --location 'http://localhost:8000/api/demo/users' \
--header 'admin-token: {ADMIN_TOKEN_ENV}' \
--header 'Content-Type: application/json' \
--data '{
    "username": "john",
    "password": "ultra-secure-password"
}'
```

### 3) Configurar oidcdebugger

No https://oidcdebugger.com/:

- `Authorization Endpoint`: `http://localhost:8000/api/authorize`
- `Token Endpoint`: `http://localhost:8000/api/token`
- `Client ID`: `<client_id>`
- `Redirect URI`: `https://oidcdebugger.com/debug` (deve bater 100% com o cadastrado)
- `Response Type`: `code`
- `Scope`: `openid profile email read`
- `Use PKCE`: habilitado (`S256`)

### 4) Executar fluxo

- Inicie o authorize no oidcdebugger.
- O servidor redireciona para `http://localhost:8000/oidcdebugger/login`.
- Faça login com o usuário criado.
- O code volta para o oidcdebugger, que troca em `/api/token`.

## Observações

- O projeto ainda não implementa `/.well-known/openid-configuration` e o endpoint `/userinfo`.
- Acamada OIDC ainda está em desenvolvimento.

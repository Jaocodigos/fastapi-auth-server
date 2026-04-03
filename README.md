# Auth Server Python

Authorization Server OAuth 2.0 (FastAPI) com fluxo `authorization_code` + PKCE (`S256`) e emissão de JWT assinados em `RS256`.

## Observações

- A IA foi utilizada para auxílio na construção de testes e do próprio README. Também usei para sanar dúvidas, mas toda lógica de negócio foi aplicada por mim,
afinal o intuito deste projeto é de fato entender como funciona na íntegra um **AS**.
- O projeto ainda não implementa `/.well-known/openid-configuration` e o endpoint `/userinfo`.
- A camada OIDC está em desenvolvimento.
- Endpoints de `revoke` e `introspect` ainda não implementados (requerem persistência de access tokens).

## Resumo rapido

- API em FastAPI com endpoints: Clients, users, scopes, claims, `authorize`, `token`, JWKS, self-registration e verificação de email.
- Persistência local (por hora) em SQLite (`app/auth.db`).
- Chaves RSA (`private.pem` / `public.pem`) geradas automaticamente no startup (se não existirem).
- Login web por cliente em `/{client_name}/login`.
- Auto-cadastro de usuários via `/{client_name}/register` com verificação de email.
- Rate limiting via `slowapi` nos endpoints de registro e verificação.
- Hashing de senhas com Argon2 (recomendação OWASP).
- Refresh token com rotação e revogação.
- Password policies por client.

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

Obrigatórias:

- `ADMIN_TOKEN_HASH`: hash SHA-256 do token de administração (veja abaixo como gerar).
- `SECRET_KEY`: secret da sessão (`SessionMiddleware`) e dos tokens de verificação de email.

### Gerando o token de admin

Execute o comando abaixo para gerar o par token/hash. Guarde o token em local seguro — apenas o hash vai para o `.env`:

```bash
python -c "import hashlib, secrets; t = secrets.token_urlsafe(32); print('Token (guarde com segurança):', t); print('Hash (ADMIN_TOKEN_HASH):', hashlib.sha256(t.encode()).hexdigest())"
```

O token gerado é usado no header `Authorization: Bearer <token>` nas chamadas à API. O hash é o valor da variável de ambiente.

Recomendadas:

- `SESSION_EXPIRE`: expiração da sessão em minutos (padrão: `30`).
- `APP_ENV`: `development` (padrão), `dev`, `prod`, `test` etc.
- `ISSUER`: valor de `iss` no JWT (também usado para montar o link de verificação de email).
- `PRIVATE_KEY_PATH`: caminho da chave privada (padrão: `private.pem`).
- `PUBLIC_KEY_PATH`: caminho da chave publica (padrão: `public.pem`).

Email (necessário para self-registration):

- `MAIL_FROM`: endereço remetente (padrão: `noreply@localhost.acme`).
- `MAIL_SERVER`: hostname do servidor SMTP (padrão: `localhost`).
- `MAIL_PORT`: porta SMTP (padrão: `1025`).
- `MAIL_USERNAME`: usuário SMTP (opcional).
- `MAIL_PASSWORD`: senha SMTP (opcional).
- `MAIL_STARTTLS`: habilitar STARTTLS (padrão: `false`).
- `MAIL_SSL_TLS`: habilitar SSL/TLS (padrão: `false`).

Exemplo (PowerShell):

```powershell
$env:ADMIN_TOKEN_HASH = "<hash-gerado-acima>"
$env:SECRET_KEY = "change-me"
$env:SESSION_EXPIRE = "30"
$env:APP_ENV = "dev"
$env:ISSUER = "http://localhost:8000"
$env:MAIL_SERVER = "localhost"
$env:MAIL_PORT = "1025"
$env:MAIL_FROM = "noreply@localhost.acme"
```

Exemplo (Linux):

```bash
export ADMIN_TOKEN_HASH="<hash-gerado-acima>"
export SECRET_KEY="change-me"
export SESSION_EXPIRE="30"
export APP_ENV="dev"
export ISSUER="http://localhost:8000"
export MAIL_SERVER="localhost"
export MAIL_PORT="1025"
export MAIL_FROM="noreply@localhost.acme"
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

**OAuth 2.0:**
- `GET /api/authorize`
- `POST /api/token`
- `GET /api/.well-known/jwks.json`

**Login:**
- `GET /{client_name}/login`
- `POST /{client_name}/login`

**Self-registration:**
- `POST /{client_name}/register` (rate limit: 3/min)
- `GET /{client_name}/verify` (rate limit: 5/min)

**Clients (admin-token):**
- `GET /api/clients`
- `POST /api/clients`
- `DELETE /api/clients/{client_id}`

**Users:**
- `GET /api/{client_name}/users` (admin-token)
- `POST /api/{client_name}/users` (admin-token)
- `DELETE /api/{client_name}/users/{username}` (admin-token)

**Scopes:**
- `GET /api/scopes`
- `POST /api/scopes`
- `DELETE /api/scopes/{scope_id}`

**Claims:**
- `GET /api/claims` (admin-token ou token)
- `POST /api/claims` (admin-token ou token)
- `DELETE /api/claims/{claim_id}` (admin-token ou token)

## Como rodar testes

Na raiz do projeto:

```powershell
.\.venv\Scripts\pytest -q
```

## Exemplo de integração com oidcdebugger.com (para testes)

### 1) Criar client OAuth

```bash
curl --location 'http://localhost:8000/api/clients' \
--header 'Authorization: Bearer {ADMIN_TOKEN}' \
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

### 2) Criar usuário para esse client

```bash
curl --location 'http://localhost:8000/api/demo/users' \
--header 'Authorization: Bearer {ADMIN_TOKEN}' \
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

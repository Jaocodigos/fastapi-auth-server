# Auth Server Python

OAuth 2.0 Authorization Server (FastAPI) with `authorization_code` + PKCE (`S256`) flow and JWT signing via `RS256`.

## Notes

- AI was used to assist in building tests and this README. It was also used to clarify doubts, but all business logic was implemented by me, as the purpose of this project is to fully understand how an **AS** works.
- The project does not yet implement `/.well-known/openid-configuration` or the `/userinfo` endpoint.
- The OIDC layer is under development.
- `revoke` and `introspect` endpoints are not yet implemented (they require access token persistence).

## Quick Overview

- FastAPI-based API with endpoints: Clients, Users, Scopes, Claims, `authorize`, `token`, JWKS, self-registration, and email verification.
- Local persistence (for now) using SQLite (`app/auth.db`).
- RSA keys (`private.pem` / `public.pem`) automatically generated on startup (if they don't exist).
- Per-client web login at `/{client_name}/login`.
- User self-registration via `/{client_name}/register` with email verification.
- Rate limiting via `slowapi` on registration and verification endpoints.
- Password hashing with Argon2 (OWASP recommendation).
- Refresh token with rotation and revocation.
- Per-client password policies.

## Requirements

- Python 3.13 (or 3.11+ with dependency adjustments)
- `pip`
- `requirements.txt`

Recommended installation:

```bash
python -m venv .venv
. .venv/Scripts/activate  # or .venv/bin/activate on Linux
pip install -r requirements.txt
```

## Environment Variables

Required:

- `ADMIN_TOKEN_HASH`: SHA-256 hash of the admin token (see below how to generate).
- `SECRET_KEY`: secret for `SessionMiddleware` and email verification tokens.

### Generating the admin token

Run the command below to generate the token/hash pair. Keep the token in a safe place — only the hash goes into `.env`:

```bash
python -c "import hashlib, secrets; t = secrets.token_urlsafe(32); print('Token (keep it safe):', t); print('Hash (ADMIN_TOKEN_HASH):', hashlib.sha256(t.encode()).hexdigest())"
```

The generated token is used in the `Authorization: Bearer <token>` header for API calls. The hash is the environment variable value.

Recommended:

- `SESSION_EXPIRE`: session expiration in minutes (default: `30`).
- `APP_ENV`: `development` (default), `dev`, `prod`, `test`, etc.
- `ISSUER`: `iss` value in the JWT (also used to build the email verification link).
- `PRIVATE_KEY_PATH`: private key path (default: `private.pem`).
- `PUBLIC_KEY_PATH`: public key path (default: `public.pem`).

Email (required for self-registration):

- `MAIL_FROM`: sender address (default: `noreply@localhost.acme`).
- `MAIL_SERVER`: SMTP server hostname (default: `localhost`).
- `MAIL_PORT`: SMTP port (default: `1025`).
- `MAIL_USERNAME`: SMTP user (optional).
- `MAIL_PASSWORD`: SMTP password (optional).
- `MAIL_STARTTLS`: enable STARTTLS (default: `false`).
- `MAIL_SSL_TLS`: enable SSL/TLS (default: `false`).

Example (PowerShell):

```powershell
$env:ADMIN_TOKEN_HASH = "<generated-hash>"
$env:SECRET_KEY = "change-me"
$env:SESSION_EXPIRE = "30"
$env:APP_ENV = "dev"
$env:ISSUER = "http://localhost:8000"
$env:MAIL_SERVER = "localhost"
$env:MAIL_PORT = "1025"
$env:MAIL_FROM = "noreply@localhost.acme"
```

Example (Linux):

```bash
export ADMIN_TOKEN_HASH="<generated-hash>"
export SECRET_KEY="change-me"
export SESSION_EXPIRE="30"
export APP_ENV="dev"
export ISSUER="http://localhost:8000"
export MAIL_SERVER="localhost"
export MAIL_PORT="1025"
export MAIL_FROM="noreply@localhost.acme"
```

## How to Run

Important: It is recommended to run the application from inside the `app` folder (if using pre-generated keys), so that the keys are generated within its scope.

```
cd app
uvicorn main:application --reload
```

Local docs:

- Swagger: `http://localhost:8000/docs`
- OpenAPI: `http://localhost:8000/openapi.json`
- JWKS: `http://localhost:8000/api/.well-known/jwks.json`

## Main Endpoints

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
- `GET /api/claims` (admin-token or token)
- `POST /api/claims` (admin-token or token)
- `DELETE /api/claims/{claim_id}` (admin-token or token)

## Running Tests

From the project root:

```powershell
.\.venv\Scripts\pytest -q
```

## Integration Example with oidcdebugger.com (for testing)

### 1) Create an OAuth client

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

Save the returned `client_id`.

### 2) Create a user for that client

```bash
curl --location 'http://localhost:8000/api/demo/users' \
--header 'Authorization: Bearer {ADMIN_TOKEN}' \
--header 'Content-Type: application/json' \
--data '{
    "username": "john",
    "password": "ultra-secure-password"
}'
```

### 3) Configure oidcdebugger

At https://oidcdebugger.com/:

- `Authorization Endpoint`: `http://localhost:8000/api/authorize`
- `Token Endpoint`: `http://localhost:8000/api/token`
- `Client ID`: `<client_id>`
- `Redirect URI`: `https://oidcdebugger.com/debug` (must match exactly what was registered)
- `Response Type`: `code`
- `Scope`: `openid profile email read`
- `Use PKCE`: enabled (`S256`)

### 4) Execute the flow

- Start the authorize flow in oidcdebugger.
- The server redirects to `http://localhost:8000/oidcdebugger/login`.
- Log in with the created user.
- The code is returned to oidcdebugger, which exchanges it at `/api/token`.

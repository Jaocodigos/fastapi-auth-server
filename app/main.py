from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.db.session import engine, Base
from app.db.app_start import seed_database
from app.core.config import validate_settings
from app.core.routing import register_controllers
from app.handlers.handler import register_error_handlers
from app.core.scripts.generate_keys import ensure_keys_exist


def create_app():

    app = FastAPI(
        title="Authorization Server",
        description="Authorization Server with both Oauth 2.0 and OpenID Connect layers.",
        version="1.0",
        contact={
            "name": "João Rodrigues",
            "github": "https://github.com/Jaocodigos"
        }
    )

    # Custom Errors
    register_error_handlers(app)

    # Import Settings
    settings = validate_settings()

    # Session middleware
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,
        max_age=settings.SESSION_EXPIRE,
        same_site="lax",
        https_only=True if settings.APP_ENV == "prod" else False,  # True on production
    )

    # Registering routes
    register_controllers(app, "app.controllers")

    # TODO: Use a relational database like MySQL or Postgres
    # Creating database(sqlite only)
    @app.on_event("startup")
    def startup():

        from app.models import User, AuthorizationCode, OAuthClient, ClientScope, ScopesAndClaims, Claims, Scopes, RefreshToken, GrantType
        Base.metadata.create_all(bind=engine)
        seed_database()
        ensure_keys_exist()


    return app



application = create_app()

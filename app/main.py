from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.controllers.authorize import router as authorize_router
from app.controllers.token import router as token_router
from app.controllers.client import router as client_router
from app.controllers.login import router as login_router
from app.controllers.user import router as user_router

from app.db.session import engine, Base
from app.core.config import validate_settings

def create_app():

    app = FastAPI()

    settings = validate_settings()

    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,
        max_age=settings.SESSION_EXPIRE,
        same_site="lax",
        https_only=True if settings.APP_ENV == "prod" else False,  # True on production
    )

    # Routes
    app.include_router(authorize_router)
    app.include_router(token_router)
    app.include_router(client_router)
    app.include_router(login_router)
    app.include_router(user_router)

    @app.on_event("startup")
    def startup():
        from app.models import User, Token, AuthorizationCode, OAuthClient
        Base.metadata.create_all(bind=engine)


    return app



application = create_app()

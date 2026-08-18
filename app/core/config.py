from pydantic import BaseModel
from os import getenv

class Settings(BaseModel):
    ADMIN_TOKEN: str = getenv("ADMIN_TOKEN_HASH")
    SESSION_EXPIRE: int = int(getenv("SESSION_EXPIRE", 30)) * 60 # Session in minutes
    SECRET_KEY: str = getenv("SECRET_KEY")
    ISSUER: str = getenv("ISSUER")
    APP_ENV: str = getenv("APP_ENV", "development")
    JWT_ALGORITHM: str = "RS256" # For now
    PRIVATE_KEY_PATH: str = getenv("PRIVATE_KEY_PATH", "private.pem")
    PUBLIC_KEY_PATH: str = getenv("PUBLIC_KEY_PATH", "public.pem")
    MAIL_FROM: str = getenv("MAIL_FROM", "noreply@localhost.acme")
    MAIL_SERVER: str = getenv("MAIL_SERVER", "localhost")
    MAIL_PORT: int = int(getenv("MAIL_PORT", 1025))
    MAIL_USERNAME: str = getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD: str = getenv("MAIL_PASSWORD", "")
    MAIL_STARTTLS: bool = getenv("MAIL_STARTTLS", "false").lower() == "true"
    MAIL_SSL_TLS: bool = getenv("MAIL_SSL_TLS", "false").lower() == "true"


settings = Settings()

def validate_settings() -> Settings:
    if not settings.ADMIN_TOKEN:
        exit("Missing ADMIN_TOKEN_HASH variable.")
    if not settings.SECRET_KEY:
        exit("Missing SECRET_KEY variable.")
    if not settings.SESSION_EXPIRE:
        exit("Missing SESSION_EXPIRE variable.")
    return settings
from pydantic import BaseModel
from os import getenv

class Settings(BaseModel):
    ADMIN_TOKEN: str = getenv("ADMIN_TOKEN")
    SESSION_EXPIRE: int = int(getenv("SESSION_EXPIRE", 30)) * 60 # Session in minutes
    SECRET_KEY: str = getenv("SECRET_KEY")
    APP_ENV: str = getenv("APP_ENV")
    ISSUER: str = getenv("ISSUER")
    APP_ENV: str = getenv("APP_ENV", "development")
    JWT_ALGORITHM: str = "RS256" # For now
    PRIVATE_KEY_PATH: str = getenv("PRIVATE_KEY_PATH", "private.pem")
    PUBLIC_KEY_PATH: str = getenv("PUBLIC_KEY_PATH", "public.pem")


settings = Settings()

def validate_settings() -> Settings:
    if not settings.ADMIN_TOKEN:
        exit("Missing ADMIN_TOKEN variable.")
    if not settings.SECRET_KEY:
        exit("Missing SECRET_KEY variable.")
    if not settings.SESSION_EXPIRE:
        exit("Missing SESSION_EXPIRE variable.")
    return settings
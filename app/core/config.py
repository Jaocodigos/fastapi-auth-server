from pydantic import BaseModel
from os import getenv

class Settings(BaseModel):
    ADMIN_TOKEN: str = getenv("ADMIN_TOKEN")
    SESSION_EXPIRE: int = int(getenv("SESSION_EXPIRE", 30)) * 60 # Session in minutes
    SECRET_KEY: str = getenv("SECRET_KEY")
    APP_ENV: str = getenv("APP_ENV")
    ISSUER: str = getenv("ISSUER")
    JWT_SECRET_KEY: str = getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256" # For now
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15


settings = Settings()

def validate_settings() -> Settings:
    if not settings.ADMIN_TOKEN:
        exit("Missing ADMIN_TOKEN variable.")
    if not settings.SECRET_KEY:
        exit("Missing SECRET_KEY variable.")
    if not settings.SESSION_EXPIRE:
        exit("Missing SESSION_EXPIRE variable.")
    return settings
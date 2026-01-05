from passlib.context import CryptContext
from app.core.config import settings
from fastapi import Header, HTTPException

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def admin_auth(admin_token: str = Header(...)):
    if admin_token != settings.ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="forbidden")


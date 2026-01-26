from app.core.config import settings
from fastapi import Header, HTTPException

def admin_auth(admin_token: str = Header(...)):
    if admin_token != settings.ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="forbidden")



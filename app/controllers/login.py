from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from typing import Annotated

from app.db.session import get_db
from app.services.security.crypt import verify_hash
from app.schemas.login import Login
from app.services.resources.client import get_client
from app.services.resources.user import get_user
from app.core.config import settings

router = APIRouter(tags=["Login"])
templates = Jinja2Templates(directory="app/templates" if settings.APP_ENV == "testing" else "templates")


@router.get("/{client_name}/login", response_class=HTMLResponse)
def login_form(client_name: str, request: Request, db: Session = Depends(get_db)):

    client = get_client(db, client_name=client_name)

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "client_name": client.name}
    )


@router.post("/{client_name}/login", response_class=HTMLResponse)
def login_submit(
    client_name: str,
    form: Annotated[Login, Form()],
    request: Request,
    db: Session = Depends(get_db),
):
    client = get_client(db, client_name=client_name)

    user = get_user(db, client_id=client.client_id, username=form.username, return_none=True)

    if not user or not verify_hash(form.password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "client_name": client.name,
                "error": "Invalid username or password.",
            },
            status_code=400,
        )

    # cria sessao
    request.session["user_id"] = user.id
    request.session["client_id"] = client.id

    # volta para authorize
    next_url = request.session.pop("next_url", "/")
    return RedirectResponse(next_url, status_code=302)

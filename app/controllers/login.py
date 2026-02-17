from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from fastapi.templating import Jinja2Templates
from typing import Annotated

from app.db.session import get_db
from app.models.user import User
from app.services.security.crypt import verify_hash
from app.schemas.login import Login

router = APIRouter(tags=["Login"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


@router.post("/login", response_class=HTMLResponse)
def login_submit(
    form: Annotated[Login, Form()],
    request: Request,
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).filter_by(username=form.username)).scalar_one_or_none()

    if not user or not verify_hash(form.password, user.password_hash):

        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid username or password.",
            },
            status_code=400,
        )

    # cria sessão
    request.session["user_id"] = user.id

    # volta para authorize
    next_url = request.session.pop("next_url", "/")
    return RedirectResponse(next_url, status_code=302)

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated


from app.db.session import get_db
from app.schemas.authorize import AuthorizeParams
from app.services.resources.oauth import generate_code

router = APIRouter(prefix="/api", tags=["Oauth 2.0"])



@router.get("/authorize")
def authorize(
    params: Annotated[AuthorizeParams, Query()],
    request: Request,
    db: Session = Depends(get_db),
):

    user_id = request.session.get("user_id")

    if not user_id:

        request.session["next_url"] = str(request.url)
        return RedirectResponse("/login", status_code=302)

    code = generate_code(user_id=user_id, data=params, db=db)

    redirect_url = f"{params.redirect_uri}?code={code}"
    if params.state:

        redirect_url += f"&state={params.state}"

    return RedirectResponse(url=redirect_url, status_code=302)

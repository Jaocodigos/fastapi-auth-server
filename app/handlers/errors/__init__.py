
from app.handlers.errors.client import ClientNotFound, InvalidClient
from app.handlers.errors.scopes import ScopeAlreadyExists, ScopeNotFound
from app.handlers.errors.claims import ClaimNotFound, ClaimAlreadyExists
from app.handlers.errors.default import OauthError, ClientError, NotFoundError, UnauthorizedError, AlreadyExistsError
from app.handlers.errors.user import UserAlreadyExists, UserNotFound

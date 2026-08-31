from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from app.models.user import User
from app.schemas.users import UserCreate, UserResponse, UserSelfRegister
from app.schemas.default import DeletedResponse
from app.services.security.crypt import hash_content
from app.handlers.errors import UserNotFound, UserAlreadyExists, UserStoreNotFound, InvalidVerificationToken, PasswordPolicyViolation
from app.services.resources.client import get_client
from app.services.email.verification import create_verification_token, decode_verification_token
from app.services.email.sender import send_verification_email
from app.handlers.errors.default import ForbiddenError


SPECIAL_CHARS = "!@#$%^&*(),.?\":{}|<>"

def get_all_users(db: Session, client_name: str):

    client = get_client(db, client_name)

    users = db.scalars(
        select(User).where(User.user_store_id == client.user_store_id).order_by(User.id)
    ).all()

    response = dict(
        users=list(
            UserResponse(id=x.id, username=x.username)
            for x in users)
    )

    return response

def get_user(db: Session, user_store_id: str, username=None, user_id=None, return_none=True) -> User | None:
    
    user_filters = [
        User.user_store_id == user_store_id,
    ]

    if username:
        user_filters.append(User.username == username)

    if user_id:
        user_filters.append(User.id == user_id)
    
    user = db.execute(select(User).where(*user_filters)
                      ).scalar_one_or_none()

    if not user:

        if return_none:
            return None

        raise UserNotFound()

    return user


def create_user(db: Session, data: UserCreate, client_name: str):

    client = get_client(db, client_name)

    exists = get_user(db, client.user_store_id, username=data.username)

    if exists:
        raise UserAlreadyExists(data.username)

    if not client.has_user_store():
        raise UserStoreNotFound()

    user = User(
        username=data.username,
        password_hash=hash_content(data.password),
        user_store_id=client.user_store_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def erase_user(db: Session, username: str, client_name: str):

    client = get_client(db, client_name)

    user = get_user(db, client.user_store_id, username=username)

    if not user:
        raise UserNotFound()

    db.delete(user)
    db.commit()

    return DeletedResponse


def validate_password_policy(password: str, policy) -> None:
    min_length = policy.min_length if policy else 8
    max_length = policy.max_length if policy else 128

    violations = []

    if len(password) < min_length:
        violations.append(f"minimum {min_length} characters")

    if len(password) > max_length:
        violations.append(f"maximum {max_length} characters")

    if policy:
        if policy.require_uppercase and not any(c.isupper() for c in password):
            violations.append("at least one uppercase letter")

        if policy.require_lowercase and not any(c.islower() for c in password):
            violations.append("at least one lowercase letter")

        if policy.require_digits and not any(c.isdigit() for c in password):
            violations.append("at least one digit")

        if policy.require_special and not any(c in SPECIAL_CHARS for c in password):
            violations.append(f"at least one special character ({SPECIAL_CHARS})")

    if violations:
        raise PasswordPolicyViolation(violations)


async def self_register(db: Session, data: UserSelfRegister, client_name: str):

    client = get_client(db, client_name)

    if client.is_confidential():
        raise ForbiddenError("Self registration is not allowed for this client.")

    validate_password_policy(data.password, client.password_policy)

    exists = get_user(db, client.user_store_id, username=data.username)
    if not exists:
        user = User(
            username=data.username,
            password_hash=hash_content(data.password),
            email=data.email,
            user_store_id=client.user_store_id,
            is_active=False
        )

        db.add(user)
        db.commit()

    token = create_verification_token(data.email)
    await send_verification_email(data.email, token, client_name)


def verify_user_email(db: Session, token: str, client_name: str):

    email = decode_verification_token(token)

    if not email:
        raise InvalidVerificationToken()

    client = get_client(db, client_name)

    user = db.execute(select(User).where(User.email == email, User.user_store_id == client.user_store_id)).scalar_one_or_none()

    if not user or user.is_active:
        return

    user.is_active = True
    db.commit()





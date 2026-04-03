from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=bool(settings.MAIL_USERNAME),
    VALIDATE_CERTS=settings.APP_ENV == "prod"
)

async def send_verification_email(email: str, token: str, client_name: str) -> None:

    verification_url = f"{settings.ISSUER}/{client_name}/verify?token={token}"

    message = MessageSchema(
        subject="Verify your email",
        recipients=[email],
        body=f"To verify your account, access the link: {verification_url}",
        subtype=MessageType.plain
    )

    fm = FastMail(conf)
    await fm.send_message(message)




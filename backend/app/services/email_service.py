import logging
from flask import current_app
from flask_mail import Message
from app.extensions import mail

log = logging.getLogger(__name__)

def send_password_reset_email(to_email: str, reset_link: str) -> None:
    server = current_app.config.get("MAIL_SERVER")
    subject = "Recuperação de senha"
    body_text = (
        "Você solicitou redefinição de senha.\n\n"
        f"Acesse o link (válido por tempo limitado):\n{reset_link}\n\n"
        "Se não foi você, ignore este e-mail."
    )

    if not server:
        if current_app.config.get("DEBUG") and current_app.config.get("LOG_RESET_TOKEN_IN_DEV"):
            log.warning(
                "SMTP não configurado — link de recuperação (apenas desenvolvimento): %s",
                reset_link,
            )
            return
        raise RuntimeError("mail_not_configured")

    msg = Message(
        subject=subject,
        recipients=[to_email],
        body=body_text,
        sender=current_app.config.get("MAIL_DEFAULT_SENDER"),
    )
    mail.send(msg)
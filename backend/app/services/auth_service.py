import hashlib
import logging
import secrets
from datetime import datetime, timedelta
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash
from app.errors import ApiError
from app.extensions import db
from app.models import PasswordResetToken, Login
from app.services.email_service import send_password_reset_email
from app.services.validation import parse_email_identifier, peek_email_identifier, require_name, require_password

log = logging.getLogger(__name__)


def register_user(data: dict) -> Login:
    name = require_name(data.get("name"))
    email = parse_email_identifier(data)
    password = require_password(data.get("password"))

    if Login.query.filter_by(email=email).first():
        raise ApiError("Este e-mail já está cadastrado.", code="email_taken", status_code=409)

    login = Login(
        email=email,
        name=name,
        password_hash=generate_password_hash(password),
    )
    db.session.add(login)
    db.session.commit()
    return login


def authenticate(data: dict) -> Login:
    email = parse_email_identifier(data)
    password = data.get("password")
    if password is None or not isinstance(password, str):
        raise ApiError("Senha é obrigatória.", code="missing_password")

    login = Login.query.filter_by(email=email).first()
    if login is None or not check_password_hash(login.password_hash, password):
        raise ApiError("E-mail ou senha incorretos.", code="invalid_credentials", status_code=401)
    return login


def _hash_reset_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def request_password_reset(data: dict) -> None:
    """Não revela se o e-mail existe; ignora identificadores inválidos."""
    email = peek_email_identifier(data or {})
    if not email:
        return

    login = Login.query.filter_by(email=email).first()
    if login is None:
        return

    raw_token = secrets.token_urlsafe(32)
    token_hash = _hash_reset_token(raw_token)
    hours = int(current_app.config.get("PASSWORD_RESET_TOKEN_HOURS", 1))
    expires = datetime.now(timezone.utc) + timedelta(hours=hours)

    row = PasswordResetToken(
        login_id=login.id,
        token_hash=token_hash,
        expires_at=expires,
    )
    db.session.add(row)
    db.session.commit()

    base = current_app.config.get("PASSWORD_RESET_FRONTEND_URL", "").rstrip("/")
    reset_link = f"{base}?token={raw_token}"

    try:
        send_password_reset_email(login.email, reset_link)
    except RuntimeError:
        if current_app.config.get("DEBUG") and current_app.config.get("LOG_RESET_TOKEN_IN_DEV"):
            log.warning("E-mail não enviado (SMTP ausente). Link dev: %s", reset_link)


def reset_password_with_token(data: dict) -> None:
    token = (data.get("token") or "").strip()
    pwd = data.get("password") if data.get("password") is not None else data.get("new_password")
    password = require_password(pwd)

    if not token:
        raise ApiError("Token inválido ou expirado.", code="invalid_token", status_code=400)

    token_hash = _hash_reset_token(token)
    row = PasswordResetToken.query.filter_by(token_hash=token_hash, used_at=None).first()

    if row is None or row.expires_at < datetime.now(timezone.utc):
        raise ApiError("Token inválido ou expirado.", code="invalid_token", status_code=400)

    login = row.login
    login.password_hash = generate_password_hash(password)
    row.used_at = datetime.now(timezone.utc)
    db.session.add(login)
    db.session.add(row)
    db.session.commit()
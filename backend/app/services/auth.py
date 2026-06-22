import logging
from datetime import datetime, timezone
from werkzeug.security import check_password_hash, generate_password_hash
from app.errors import ApiError
from app.extensions import db
from app.models import Login
from app.services.validation import parse_email_identifier, require_name, require_password

log = logging.getLogger(__name__)

def register_user(data: dict) -> Login:
    name = require_name(data.get("name"))
    email = parse_email_identifier(data)
    password = require_password(data.get("password"))

    if data.get("consent_accepted") is not True:
        raise ApiError("E necessario aceitar o termo de consentimento para criar uma conta.", code="consent_required")

    if email is None:
        raise ApiError("E-mail é obrigatório.", code="missing_email")

    if Login.query.filter_by(email=email).first():
        raise ApiError("Este e-mail já está cadastrado.", code="email_taken", status_code=409)

    login = Login(
        email=email,
        name=name,
        password=generate_password_hash(password),
        consent_accepted_at=datetime.now(timezone.utc),
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

    if login is None or not check_password_hash(login.password, password):
        raise ApiError("E-mail ou senha incorretos.", code="invalid_credentials", status_code=401)

    return login


def get_user(login_id: int) -> Login:
    user = db.session.get(Login, login_id)
    if user is None:
        raise ApiError("Usuario nao encontrado.", code="user_not_found", status_code=404)
    return user


def update_user(login_id: int, data: dict) -> Login:
    user = get_user(login_id)
    updated = False

    if "name" in data:
        user.name = require_name(data.get("name"))
        updated = True

    if "email" in data:
        email = parse_email_identifier(data)
        duplicate = Login.query.filter(Login.email == email, Login.id != user.id).first()
        if duplicate is not None:
            raise ApiError("Este e-mail ja esta cadastrado.", code="email_taken", status_code=409)
        user.email = email
        updated = True

    new_password = data.get("new_password")
    if new_password is not None:
        current_password = data.get("current_password")
        if not isinstance(current_password, str) or not check_password_hash(user.password, current_password):
            raise ApiError(
                "Informe a senha atual para altera-la.",
                code="invalid_current_password",
                status_code=401,
            )
        user.password = generate_password_hash(require_password(new_password))
        updated = True

    if not updated:
        raise ApiError("Informe ao menos um dado para atualizar.", code="no_changes")

    db.session.commit()
    log.info("Perfil atualizado: user_id=%s", user.id)
    return user


def delete_user(login_id: int, password: str | None) -> None:
    user = get_user(login_id)
    if not isinstance(password, str) or not check_password_hash(user.password, password):
        raise ApiError("Senha atual incorreta.", code="invalid_credentials", status_code=401)

    db.session.delete(user)
    db.session.commit()
    log.info("Conta excluida: user_id=%s", login_id)


def list_participants(login_id: int, search: str | None = None, limit: int = 30) -> list[Login]:
    query = Login.query.filter(Login.id != login_id)
    normalized_search = (search or "").strip()
    if normalized_search:
        query = query.filter(Login.name.ilike(f"%{normalized_search}%"))

    return query.order_by(Login.name.asc()).limit(min(max(limit, 1), 50)).all()

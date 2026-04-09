import logging
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

    if email is None:
        raise ApiError("E-mail é obrigatório.", code="missing_email")

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
import re
from email_validator import EmailNotValidError, validate_email
from app.errors import ApiError

_PASSWORD_MIN = 8

def parse_email_identifier(data: dict) -> str:
    raw = (data.get("email") or "").strip()

    if not raw:
        raise ApiError("Informe e-mail.", code="missing_identifier")

    try:
        normalized = validate_email(raw, check_deliverability=False).normalized
    except EmailNotValidError:
        raise ApiError("E-mail inválido.", code="invalid_email")

    return normalized.lower()


def require_password(password: str | None) -> str:
    if password is None or not isinstance(password, str):
        raise ApiError("Senha é obrigatória.", code="missing_password")

    if len(password) < _PASSWORD_MIN:
        raise ApiError(f"A senha deve ter pelo menos {_PASSWORD_MIN} caracteres.", code="invalid_password")

    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        raise ApiError("A senha deve conter pelo menos uma letra e um número.", code="invalid_password")

    return password

def require_name(name: str | None) -> str:
    if name is None or not str(name).strip():
        raise ApiError("Nome é obrigatório.", code="missing_name")

    if len(name) > 255:
        raise ApiError("Nome muito longo.", code="invalid_name")

    return name
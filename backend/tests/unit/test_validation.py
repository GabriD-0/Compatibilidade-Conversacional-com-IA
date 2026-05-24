import pytest
from app.errors import ApiError
from app.services.validation import parse_email_identifier, require_name, require_password


@pytest.mark.unit
def test_parse_email_identifier_normalizes_email():
    assert parse_email_identifier({"email": " USER@Example.COM "}) == "user@example.com"


@pytest.mark.unit
@pytest.mark.parametrize(
    ("payload", "code"),
    [
        ({}, "missing_identifier"),
        ({"email": "   "}, "missing_identifier"),
        ({"email": "not-an-email"}, "invalid_email"),
    ],
)
def test_parse_email_identifier_rejects_invalid_input(payload, code):
    with pytest.raises(ApiError) as exc_info:
        parse_email_identifier(payload)

    assert exc_info.value.code == code


@pytest.mark.unit
def test_require_password_accepts_valid_password():
    assert require_password("abc12345") == "abc12345"


@pytest.mark.unit
@pytest.mark.parametrize(
    ("password", "code"),
    [
        (None, "missing_password"),
        (12345678, "missing_password"),
        ("abc123", "invalid_password"),
        ("abcdefgh", "invalid_password"),
        ("12345678", "invalid_password"),
    ],
)
def test_require_password_rejects_invalid_passwords(password, code):
    with pytest.raises(ApiError) as exc_info:
        require_password(password)

    assert exc_info.value.code == code


@pytest.mark.unit
def test_require_name_accepts_non_empty_name():
    assert require_name("Alice") == "Alice"


@pytest.mark.unit
@pytest.mark.parametrize(
    ("name", "code"),
    [
        (None, "missing_name"),
        ("   ", "missing_name"),
        ("a" * 256, "invalid_name"),
    ],
)
def test_require_name_rejects_invalid_names(name, code):
    with pytest.raises(ApiError) as exc_info:
        require_name(name)

    assert exc_info.value.code == code

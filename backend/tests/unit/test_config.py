import pytest
from app.config import _bool_env, build_sqlalchemy_uri


@pytest.mark.unit
def test_build_sqlalchemy_uri_encodes_password():
    uri = build_sqlalchemy_uri(
        user="user",
        password="p@ss word",
        host="localhost",
        port=5432,
        database="database",
    )

    assert uri == "postgresql+psycopg2://user:p%40ss+word@localhost:5432/database"


@pytest.mark.unit
@pytest.mark.parametrize("value", ["1", "true", "TRUE", "yes", "on"])
def test_bool_env_true_values(monkeypatch, value):
    monkeypatch.setenv("FEATURE_FLAG", value)

    assert _bool_env("FEATURE_FLAG") is True


@pytest.mark.unit
@pytest.mark.parametrize("value", ["0", "false", "no", "off", "anything"])
def test_bool_env_false_values(monkeypatch, value):
    monkeypatch.setenv("FEATURE_FLAG", value)

    assert _bool_env("FEATURE_FLAG") is False


@pytest.mark.unit
def test_bool_env_uses_default_when_missing(monkeypatch):
    monkeypatch.delenv("FEATURE_FLAG", raising=False)

    assert _bool_env("FEATURE_FLAG", default=True) is True

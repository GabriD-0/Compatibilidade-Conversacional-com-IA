import pytest
from types import SimpleNamespace
from app.errors import ApiError
from app.services import auth


class FakeQuery:
    def __init__(self, result=None):
        self.result = result
        self.filters = []

    def filter_by(self, **kwargs):
        self.filters.append(kwargs)
        return self

    def first(self):
        return self.result


class FakeSession:
    def __init__(self, result=None):
        self.result = result
        self.added = None
        self.deleted = None
        self.committed = False

    def add(self, item):
        self.added = item

    def get(self, _model, _identifier):
        return self.result

    def delete(self, item):
        self.deleted = item

    def commit(self):
        self.committed = True


@pytest.mark.unit
def test_register_user_persists_normalized_user(monkeypatch):
    query = FakeQuery()
    session = FakeSession()

    class FakeLogin:
        def __init__(self, email, name, password, consent_accepted_at=None):
            self.email = email
            self.name = name
            self.password = password
            self.consent_accepted_at = consent_accepted_at

    FakeLogin.query = query
    monkeypatch.setattr(auth, "Login", FakeLogin)
    monkeypatch.setattr(auth, "db", SimpleNamespace(session=session))
    monkeypatch.setattr(auth, "generate_password_hash", lambda password: f"hash:{password}")

    user = auth.register_user(
        {
            "email": " USER@Example.COM ",
            "name": "Alice",
            "password": "abc12345",
            "consent_accepted": True,
        }
    )

    assert query.filters == [{"email": "user@example.com"}]
    assert user.email == "user@example.com"
    assert user.name == "Alice"
    assert user.password == "hash:abc12345"
    assert session.added is user
    assert session.committed is True


@pytest.mark.unit
def test_register_user_rejects_duplicate_email(monkeypatch):
    duplicate = SimpleNamespace(id=1, email="user@example.com")

    class FakeLogin:
        query = FakeQuery(duplicate)

    monkeypatch.setattr(auth, "Login", FakeLogin)

    with pytest.raises(ApiError) as exc_info:
        auth.register_user(
            {
                "email": "user@example.com",
                "name": "Alice",
                "password": "abc12345",
                "consent_accepted": True,
            }
        )

    assert exc_info.value.code == "email_taken"
    assert exc_info.value.status_code == 409


@pytest.mark.unit
def test_register_user_requires_consent():
    with pytest.raises(ApiError) as exc_info:
        auth.register_user(
            {"email": "user@example.com", "name": "Alice", "password": "abc12345"}
        )

    assert exc_info.value.code == "consent_required"


@pytest.mark.unit
def test_authenticate_requires_password():
    with pytest.raises(ApiError) as exc_info:
        auth.authenticate({"email": "user@example.com"})

    assert exc_info.value.code == "missing_password"


@pytest.mark.unit
def test_authenticate_returns_user_when_credentials_match(monkeypatch):
    user = SimpleNamespace(id=1, email="user@example.com", password="stored-hash")

    class FakeLogin:
        query = FakeQuery(user)

    monkeypatch.setattr(auth, "Login", FakeLogin)
    monkeypatch.setattr(
        auth,
        "check_password_hash",
        lambda stored, provided: stored == "stored-hash" and provided == "abc12345",
    )

    assert auth.authenticate({"email": "USER@example.com", "password": "abc12345"}) is user


@pytest.mark.unit
@pytest.mark.parametrize(
    ("query_result", "password_matches"),
    [(None, True), (SimpleNamespace(password="stored-hash"), False)],
)
def test_authenticate_rejects_invalid_credentials(monkeypatch, query_result, password_matches):
    class FakeLogin:
        query = FakeQuery(query_result)

    monkeypatch.setattr(auth, "Login", FakeLogin)
    monkeypatch.setattr(auth, "check_password_hash", lambda _stored, _provided: password_matches)

    with pytest.raises(ApiError) as exc_info:
        auth.authenticate({"email": "user@example.com", "password": "abc12345"})

    assert exc_info.value.code == "invalid_credentials"
    assert exc_info.value.status_code == 401


@pytest.mark.unit
def test_update_user_updates_name_without_requiring_password(monkeypatch):
    user = SimpleNamespace(id=1, name="Alice", email="alice@example.com", password="stored")
    session = FakeSession(user)
    monkeypatch.setattr(auth, "db", SimpleNamespace(session=session))

    updated = auth.update_user(1, {"name": "Alice Silva"})

    assert updated is user
    assert user.name == "Alice Silva"
    assert session.committed is True


@pytest.mark.unit
def test_update_user_requires_current_password_for_new_password(monkeypatch):
    user = SimpleNamespace(id=1, name="Alice", email="alice@example.com", password="stored")
    monkeypatch.setattr(auth, "db", SimpleNamespace(session=FakeSession(user)))
    monkeypatch.setattr(auth, "check_password_hash", lambda _stored, _provided: False)

    with pytest.raises(ApiError) as exc_info:
        auth.update_user(1, {"current_password": "wrong", "new_password": "abc12345"})

    assert exc_info.value.code == "invalid_current_password"


@pytest.mark.unit
def test_delete_user_requires_password_and_deletes_resolved_user(monkeypatch):
    user = SimpleNamespace(id=1, password="stored")
    session = FakeSession(user)
    monkeypatch.setattr(auth, "db", SimpleNamespace(session=session))
    monkeypatch.setattr(auth, "check_password_hash", lambda stored, provided: stored == "stored" and provided == "abc12345")

    auth.delete_user(1, "abc12345")

    assert session.deleted is user
    assert session.committed is True

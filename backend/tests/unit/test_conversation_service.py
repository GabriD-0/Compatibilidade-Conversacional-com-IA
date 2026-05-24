import pytest
from types import SimpleNamespace
from app.errors import ApiError
from app.services import conversation


class FakeSession:
    def __init__(self, result=None):
        self.result = result
        self.deleted = None
        self.executed = None
        self.committed = False

    def get(self, _model, _identifier):
        return self.result

    def delete(self, item):
        self.deleted = item

    def execute(self, statement):
        self.executed = statement

    def commit(self):
        self.committed = True


@pytest.mark.unit
@pytest.mark.parametrize(
    ("content", "code"),
    [("", "empty_content"), ("   ", "empty_content"), ("x" * 5001, "content_too_long")],
)
def test_persist_message_validates_content_before_database_write(content, code):
    with pytest.raises(ApiError) as exc_info:
        conversation.persist_message(1, 1, content)

    assert exc_info.value.code == code


@pytest.mark.unit
def test_get_conversation_returns_owned_conversation(monkeypatch):
    conv = SimpleNamespace(id=10, participant_a_id=1, participant_b_id=2)
    monkeypatch.setattr(conversation, "db", SimpleNamespace(session=FakeSession(conv)))

    assert conversation.get_conversation(1, 10) is conv
    assert conversation.get_conversation(2, 10) is conv


@pytest.mark.unit
@pytest.mark.parametrize(
    "stored_conversation",
    [None, SimpleNamespace(id=10, participant_a_id=1, participant_b_id=2)],
)
def test_get_conversation_rejects_missing_or_unowned_conversation(monkeypatch, stored_conversation):
    monkeypatch.setattr(
        conversation,
        "db",
        SimpleNamespace(session=FakeSession(stored_conversation)),
    )

    with pytest.raises(ApiError) as exc_info:
        conversation.get_conversation(3, 10)

    assert exc_info.value.code == "not_found"
    assert exc_info.value.status_code == 404


@pytest.mark.unit
def test_create_conversation_rejects_missing_explicit_participant(monkeypatch):
    monkeypatch.setattr(conversation, "db", SimpleNamespace(session=FakeSession(None)))

    with pytest.raises(ApiError) as exc_info:
        conversation.create_conversation(1, {"participant_id": 2})

    assert exc_info.value.code == "user_not_found"
    assert exc_info.value.status_code == 404


@pytest.mark.unit
def test_create_conversation_rejects_self_conversation(monkeypatch):
    monkeypatch.setattr(
        conversation,
        "db",
        SimpleNamespace(session=FakeSession(SimpleNamespace(id=1))),
    )

    with pytest.raises(ApiError) as exc_info:
        conversation.create_conversation(1, {"participant_id": 1})

    assert exc_info.value.code == "self_conversation"


@pytest.mark.unit
def test_delete_conversation_deletes_resolved_conversation(monkeypatch):
    conv = SimpleNamespace(id=10)
    session = FakeSession()
    monkeypatch.setattr(conversation, "get_conversation", lambda _login_id, _conversation_id: conv)
    monkeypatch.setattr(conversation, "db", SimpleNamespace(session=session))

    conversation.delete_conversation(1, 10)

    assert session.deleted is conv
    assert session.committed is True


@pytest.mark.unit
def test_mark_read_executes_update_and_commits(monkeypatch):
    session = FakeSession()
    monkeypatch.setattr(conversation, "db", SimpleNamespace(session=session))

    conversation.mark_read(conversation_id=1, reader_id=2, up_to_position=5)

    assert session.executed is not None
    assert session.committed is True

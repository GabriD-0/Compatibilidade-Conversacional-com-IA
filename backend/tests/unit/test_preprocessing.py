import pytest
from datetime import datetime, timezone
from app.core.preprocessing import canonicalize_token, group_by_sender, normalize_multiword_tokens, normalize_text, prepare_messages, strip_accents, tokenize


@pytest.mark.unit
def test_normalize_text_collapses_spacing_and_casefolds():
    assert normalize_text("  Ol\u00e1\tMUNDO\n ") == "ol\u00e1 mundo"


@pytest.mark.unit
def test_strip_accents_and_canonicalize_token():
    assert strip_accents("a\u00e7\u00e3o") == "acao"
    assert canonicalize_token("Voc\u00ea") == "voce"


@pytest.mark.unit
def test_tokenize_preserves_supported_word_shapes():
    assert tokenize("Ol\u00e1, voc\u00ea vai por que? 123 teste-final") == [
        "ol\u00e1",
        "voc\u00ea",
        "vai",
        "por",
        "que",
        "123",
        "teste-final",
    ]


@pytest.mark.unit
def test_normalize_multiword_tokens_merges_por_que():
    assert normalize_multiword_tokens(["Por", "QUE", "Voc\u00ea"]) == ["porque", "voce"]


@pytest.mark.unit
def test_prepare_messages_sorts_and_derives_text_fields(raw_message_factory):
    first = raw_message_factory(
        id=1,
        position=1,
        sender_id=2,
        content=" Voc\u00ea vai por que? ",
        sent_at=datetime(2026, 1, 1, 12, 1, tzinfo=timezone.utc),
    )
    second = raw_message_factory(
        id=2,
        position=0,
        sender_id=1,
        content="Ol\u00e1 mundo",
        sent_at=datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc),
    )

    prepared = prepare_messages([first, second])

    assert [message.id for message in prepared] == [2, 1]
    assert prepared[0].normalized_content == "ol\u00e1 mundo"
    assert prepared[0].tokens == ["ol\u00e1", "mundo"]
    assert prepared[0].canonical_tokens == ["ola", "mundo"]
    assert prepared[0].word_count == 2
    assert prepared[1].canonical_tokens == ["voce", "vai", "porque"]


@pytest.mark.unit
@pytest.mark.parametrize(
    ("content", "sent_at", "expected_message"),
    [
        ("   ", datetime(2026, 1, 1, tzinfo=timezone.utc), "conteudo vazio"),
        ("Ola", None, "sem timestamp"),
    ],
)
def test_prepare_messages_rejects_invalid_messages(
    raw_message_factory,
    content,
    sent_at,
    expected_message,
):
    message = raw_message_factory(content=content, sent_at=sent_at)
    if sent_at is None:
        message.sent_at = None

    with pytest.raises(ValueError, match=expected_message):
        prepare_messages([message])


@pytest.mark.unit
def test_group_by_sender_groups_prepared_messages(raw_message_factory):
    messages = prepare_messages(
        [
            raw_message_factory(id=1, sender_id=1, position=0),
            raw_message_factory(id=2, sender_id=2, position=1),
            raw_message_factory(id=3, sender_id=1, position=2),
        ]
    )

    grouped = group_by_sender(messages)

    assert list(grouped) == [1, 2]
    assert [message.id for message in grouped[1]] == [1, 3]
    assert [message.id for message in grouped[2]] == [2]

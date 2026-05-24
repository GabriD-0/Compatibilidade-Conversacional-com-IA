import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

WORD_REGEX = re.compile(r"[0-9A-Za-zÀ-ÖØ-öø-ÿ]+(?:['-][0-9A-Za-zÀ-ÖØ-öø-ÿ]+)?")
SPACE_REGEX = re.compile(r"\s+")


@dataclass(frozen=True)
class PreparedMessage:
    id: int | None
    position: int
    sender_id: int
    content: str
    sent_at: datetime
    normalized_content: str
    tokens: list[str]
    canonical_tokens: list[str]
    word_count: int
    char_count: int


def normalize_text(text: str) -> str:
    """Normalize spacing and case while preserving Portuguese accents."""
    normalized = unicodedata.normalize("NFKC", text or "")
    normalized = SPACE_REGEX.sub(" ", normalized.strip())
    return normalized.casefold()


def strip_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def canonicalize_token(token: str) -> str:
    return strip_accents(token.casefold())


def tokenize(text: str) -> list[str]:
    return WORD_REGEX.findall(normalize_text(text))


def normalize_multiword_tokens(tokens: list[str]) -> list[str]:
    """Normaliza tokens multi-palavras como 'por que' para 'porque'."""
    normalized = []
    index = 0

    while index < len(tokens):
        current_token = canonicalize_token(tokens[index])

        if (current_token == "por"and index + 1 < len(tokens) and canonicalize_token(tokens[index + 1]) == "que"):
            normalized.append("porque")
            index += 2
            continue

        normalized.append(current_token)
        index += 1

    return normalized


def prepare_messages(messages: Iterable[object]) -> list[PreparedMessage]:
    prepared: list[PreparedMessage] = []

    for msg in sorted(messages, key=lambda item: getattr(item, "position", 0)):
        content = getattr(msg, "content", None)
        sent_at = getattr(msg, "sent_at", None)

        if not isinstance(content, str) or not content.strip():
            raise ValueError("Mensagem com conteudo vazio nao pode ser analisada.")

        if sent_at is None:
            raise ValueError("Mensagem sem timestamp nao pode ser analisada.")

        normalized = normalize_text(content)
        tokens = tokenize(content)

        prepared.append(
            PreparedMessage(
                id=getattr(msg, "id", None),
                position=int(getattr(msg, "position")),
                sender_id=int(getattr(msg, "sender_id")),
                content=content.strip(),
                sent_at=sent_at,
                normalized_content=normalized,
                tokens=tokens,
                canonical_tokens=normalize_multiword_tokens(tokens),
                word_count=len(tokens),
                char_count=len(content.strip()),
            )
        )

    return prepared


def group_by_sender(messages: Iterable[PreparedMessage]) -> dict[int, list[PreparedMessage]]:
    grouped: dict[int, list[PreparedMessage]] = {}
    for message in messages:
        grouped.setdefault(message.sender_id, []).append(message)

    return grouped

import os
import pytest
from datetime import datetime, timezone
from types import SimpleNamespace

# Definindo variaveis de ambiente para os testes
os.environ.setdefault("DB_USER", "test")
os.environ.setdefault("DB_PASSWORD", "test")
os.environ.setdefault("DB_NAME", "test")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("SSH_PORT", "22")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:3000")
os.environ.setdefault("SENTIMENT_MODEL_NAME", "unit-test-model")
os.environ.setdefault("SENTIMENT_MODEL_DEVICE", "-1")
os.environ.setdefault("SENTIMENT_BATCH_SIZE", "2")
os.environ.setdefault("SENTIMENT_MAX_LENGTH", "128")


@pytest.fixture
def raw_message_factory():
    def factory(
        *,
        id=1,
        position=0,
        sender_id=1,
        content="Ola mundo",
        sent_at=None,
    ):
        return SimpleNamespace(
            id=id,
            position=position,
            sender_id=sender_id,
            content=content,
            sent_at=sent_at or datetime(2026, 1, 1, tzinfo=timezone.utc),
        )

    return factory

import os
from dataclasses import dataclass
from transformers import pipeline
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from flask import current_app, has_app_context
from app.core.preprocessing import PreparedMessage

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

SENTIMENT_MODEL_NAME = os.environ.get("SENTIMENT_MODEL_NAME")
SENTIMENT_MODEL_DEVICE = int(os.environ.get("SENTIMENT_MODEL_DEVICE"))
SENTIMENT_BATCH_SIZE = int(os.environ.get("SENTIMENT_BATCH_SIZE"))
SENTIMENT_MAX_LENGTH = int(os.environ.get("SENTIMENT_MAX_LENGTH"))

MODEL_LABEL_POLARITY: dict[str, float] = {
    "Very Negative": -1.0,
    "Negative": -0.5,
    "Neutral": 0.0,
    "Positive": 0.5,
    "Very Positive": 1.0,
}

MODEL_LABEL_ALIASES: dict[str, str] = {
    "label 0": "Very Negative",
    "label 1": "Negative",
    "label 2": "Neutral",
    "label 3": "Positive",
    "label 4": "Very Positive",
    "very negative": "Very Negative",
    "negative": "Negative",
    "neutral": "Neutral",
    "positive": "Positive",
    "very positive": "Very Positive",
}

DEFAULT_ANALYZER_CACHE: dict[tuple[Any, ...], "SentimentAnalyzer"] = {}


@dataclass(frozen=True)
class SentimentResult:
    message_id: int | None
    position: int
    sender_id: int
    label: str
    polarity: float
    intensity: float
    evidence_count: int
    confidence: float | None = None
    source_label: str | None = None

    def to_dict(self) -> dict:
        payload = {
            "message_id": self.message_id,
            "position": self.position,
            "sender_id": self.sender_id,
            "label": self.label,
            "polarity": self.polarity,
            "intensity": self.intensity,
            "evidence_count": self.evidence_count,
        }
        if self.confidence is not None:
            payload["confidence"] = self.confidence
        if self.source_label is not None:
            payload["source_label"] = self.source_label
        return payload

class SentimentAnalyzer:
    def analyze_message(self, message: PreparedMessage) -> SentimentResult:
        raise NotImplementedError

    def metadata(self) -> dict:
        return {}

    def analyze_messages(self, messages: list[PreparedMessage], participant_ids: tuple[int, int]) -> dict:
        message_results = [self.analyze_message(message) for message in messages]

        return build_sentiment_metrics(message_results, participant_ids, metadata=self.metadata())

class HuggingFaceSentimentAnalyzer(SentimentAnalyzer):
    def __init__(
        self,
        model_name: str = SENTIMENT_MODEL_NAME,
        device: int = SENTIMENT_MODEL_DEVICE,
        batch_size: int = SENTIMENT_BATCH_SIZE,
        max_length: int = SENTIMENT_MAX_LENGTH,
    ) -> None:
        self.model_name = model_name
        self.device = device
        self.batch_size = max(1, batch_size)
        self.max_length = max(1, max_length)
        self._classifier = None

    def metadata(self) -> dict:
        return {
            "provider": "huggingface",
            "model_name": self.model_name,
            "label_space": list(MODEL_LABEL_POLARITY.keys()),
            "max_length": self.max_length,
        }

    def analyze_message(self, message: PreparedMessage) -> SentimentResult:
        outputs = self.run_pipeline([message.content])
        return self._result_from_output(message, outputs[0])

    def analyze_messages(self, messages: list[PreparedMessage], participant_ids: tuple[int, int]) -> dict:
        if not messages:
            return build_sentiment_metrics([], participant_ids, metadata=self.metadata())

        outputs = self.run_pipeline([message.content for message in messages])
        results = [
            self._result_from_output(message, output)
            for message, output in zip(messages, outputs)
        ]

        return build_sentiment_metrics(results, participant_ids, metadata=self.metadata())

    def _get_classifier(self):
        if self._classifier is not None:
            return self._classifier

        try:
            self._classifier = pipeline(
                "text-classification",
                model=self.model_name,
                tokenizer=self.model_name,
                device=self.device,
            )
        except Exception as exc:
            raise RuntimeError(f"Nao foi possivel carregar o modelo de sentimento '{self.model_name}'.") from exc

        return self._classifier

    def run_pipeline(self, texts: list[str]) -> list[dict]:
        try:
            raw_outputs = self._get_classifier()(
                texts,
                batch_size=self.batch_size,
                truncation=True,
                max_length=self.max_length,
            )
        except RuntimeError:
            raise
        except Exception as exc:
            raise RuntimeError("Falha ao executar o modelo de sentimento.") from exc

        return normalize_pipeline_outputs(raw_outputs, expected_count=len(texts))

    def _result_from_output(self, message: PreparedMessage, output: dict) -> SentimentResult:
        source_label = str(output.get("label", "Neutral"))
        confidence = min_max(float(output.get("score", 0.0)), 0.0, 1.0)
        model_label = canonical_model_label(source_label)
        polarity = MODEL_LABEL_POLARITY[model_label]
        label = label_from_polarity(polarity)

        return SentimentResult(
            message_id=message.id,
            position=message.position,
            sender_id=message.sender_id,
            label=label,
            polarity=round(polarity, 4),
            intensity=round(abs(polarity), 4),
            evidence_count=1,
            confidence=round(confidence, 4),
            source_label=model_label,
        )


def get_SENTIMENT_ANALYZER() -> SentimentAnalyzer:
    model_name = str(get_config_value("SENTIMENT_MODEL_NAME", SENTIMENT_MODEL_NAME))
    device = get_int_config_value("SENTIMENT_MODEL_DEVICE", SENTIMENT_MODEL_DEVICE)
    batch_size = get_int_config_value("SENTIMENT_BATCH_SIZE", SENTIMENT_BATCH_SIZE)
    max_length = get_int_config_value("SENTIMENT_MAX_LENGTH", SENTIMENT_MAX_LENGTH)
    cache_key = ("hf", model_name, device, batch_size, max_length)

    if cache_key not in DEFAULT_ANALYZER_CACHE:
        DEFAULT_ANALYZER_CACHE[cache_key] = HuggingFaceSentimentAnalyzer(
            model_name=model_name,
            device=device,
            batch_size=batch_size,
            max_length=max_length,
        )

    return DEFAULT_ANALYZER_CACHE[cache_key]


def analyze_sentiments(messages: list[PreparedMessage], participant_ids: tuple[int, int], analyzer: SentimentAnalyzer | None = None) -> dict:
    selected_analyzer = analyzer or get_SENTIMENT_ANALYZER()

    return selected_analyzer.analyze_messages(messages, participant_ids)


def build_sentiment_metrics(message_results: list[SentimentResult], participant_ids: tuple[int, int], metadata: dict | None = None) -> dict:
    participant_metrics = {
        str(participant_id): summarize_results([result for result in message_results if result.sender_id == participant_id])
        for participant_id in participant_ids
    }

    first = participant_metrics[str(participant_ids[0])]
    second = participant_metrics[str(participant_ids[1])]
    polarity_distance = abs(first["average_polarity"] - second["average_polarity"]) / 2
    intensity_distance = abs(first["average_intensity"] - second["average_intensity"])
    participant_convergence = max(
        0.0,
        1 - (0.7 * polarity_distance + 0.3 * intensity_distance),
    )
    turn_convergence = calculate_turn_convergence(message_results)
    score = round((0.6 * participant_convergence + 0.4 * turn_convergence) * 100, 2)

    payload = {
        "score": score,
        "participants": participant_metrics,
        "conversation": {
            "average_polarity": round(
                sum(result.polarity for result in message_results)
                / max(len(message_results), 1),
                4,
            ),
            "average_intensity": round(
                sum(result.intensity for result in message_results)
                / max(len(message_results), 1),
                4,
            ),
            "participant_convergence": round(participant_convergence * 100, 2),
            "turn_convergence": round(turn_convergence * 100, 2),
        },
        "messages": [result.to_dict() for result in message_results],
    }
    payload.update(metadata or {})
    return payload


def summarize_results(results: list[SentimentResult]) -> dict:
    total = len(results)
    distribution = {"positive": 0, "neutral": 0, "negative": 0}
    for result in results:
        distribution[result.label] += 1

    return {
        "message_count": total,
        "average_polarity": round(sum(result.polarity for result in results) / max(total, 1), 4),
        "average_intensity": round(sum(result.intensity for result in results) / max(total, 1), 4),
        "distribution": distribution,
    }


def calculate_turn_convergence(results: list[SentimentResult]) -> float:
    similarities: list[float] = []

    for previous, current in zip(results, results[1:]):
        if previous.sender_id == current.sender_id:
            continue
        similarities.append(1 - (abs(previous.polarity - current.polarity) / 2))

    if not similarities:
        return 0.5

    return min_max(sum(similarities) / len(similarities), 0.0, 1.0)


def normalize_pipeline_outputs(raw_outputs: Any, expected_count: int) -> list[dict]:
    if expected_count == 1 and isinstance(raw_outputs, dict):
        return [raw_outputs]

    if not isinstance(raw_outputs, list):
        raise RuntimeError("Resposta invalida do modelo de sentimento.")

    outputs = raw_outputs
    if expected_count == 1 and outputs and isinstance(outputs[0], dict):
        return [outputs[0]]

    normalized: list[dict] = []
    for output in outputs:
        if isinstance(output, dict):
            normalized.append(output)
            continue

        if isinstance(output, list) and output:
            best = max(output, key=lambda item: float(item.get("score", 0.0)))
            normalized.append(best)
            continue

        raise RuntimeError("Item invalido na resposta do modelo de sentimento.")

    if len(normalized) != expected_count:
        raise RuntimeError("Quantidade inesperada de resultados do modelo de sentimento.")

    return normalized


def canonical_model_label(label: str) -> str:
    normalized = label.replace("_", " ").strip().lower()
    model_label = MODEL_LABEL_ALIASES.get(normalized)
    if model_label is None:
        raise RuntimeError(f"Rotulo de sentimento desconhecido: {label}")
    return model_label


def get_config_value(name: str, default: Any) -> Any:
    if has_app_context():
        return current_app.config.get(name, default)
    return os.environ.get(name, default)


def get_int_config_value(name: str, default: int) -> int:
    value = get_config_value(name, default)
    if value is None or str(value).strip() == "":
        return default
    return int(value)


def label_from_polarity(polarity: float) -> str:
    if polarity >= 0.15:
        return "positive"
    if polarity <= -0.15:
        return "negative"
    return "neutral"


def min_max(value: float, minimum: float, maximum: float) -> float:
    """Limita um valor para que fique dentro de um intervalo definido por mínimo e máximo."""
    return max(minimum, min(maximum, value))


from statistics import mean
from app.core.preprocessing import PreparedMessage

def calculate_behavioral_signs(messages: list[PreparedMessage], participant_ids: tuple[int, int]) -> dict:
    """Calcula sinais comportamentais com base em mensagens pré-processadas e IDs dos participantes."""
    message_counts = {
        participant_id: len([message for message in messages if message.sender_id == participant_id])
        for participant_id in participant_ids
    }

    word_lengths = {
        participant_id: [message.word_count for message in messages if message.sender_id == participant_id]
        for participant_id in participant_ids
    }

    response_times = calculate_response_times(messages, participant_ids)

    turn_balance = balance_score(message_counts[participant_ids[0]], message_counts[participant_ids[1]])

    length_balance = balance_score(
        mean_or_zero(word_lengths[participant_ids[0]]),
        mean_or_zero(word_lengths[participant_ids[1]]),
    )

    response_balance = balance_score(
        mean_or_zero(response_times[participant_ids[0]]),
        mean_or_zero(response_times[participant_ids[1]]),
        neutral_when_empty=True,
    )

    response_speed = response_speed_score([seconds for values in response_times.values() for seconds in values])

    score = round(
        0.35 * turn_balance
        + 0.25 * length_balance
        + 0.25 * response_balance
        + 0.15 * response_speed,
        2,
    )

    return {
        "score": score,
        "turn_balance": round(turn_balance, 2),
        "length_balance": round(length_balance, 2),
        "response_time_balance": round(response_balance, 2),
        "response_speed": round(response_speed, 2),
        "participants": {
            str(participant_id): {
                "message_count": message_counts[participant_id],
                "average_message_length_words": round(
                    mean_or_zero(word_lengths[participant_id]),
                    2,
                ),
                "average_response_time_seconds": round_or_none(mean_or_none(response_times[participant_id])),
                "response_count": len(response_times[participant_id]),
            }
            for participant_id in participant_ids
        },
        "conversation": {
            "message_count": len(messages),
            "average_message_length_words": round(
                mean_or_zero([message.word_count for message in messages]),
                2,
            ),
            "average_response_time_seconds": round_or_none(
                mean_or_none([seconds for values in response_times.values() for seconds in values])
            ),
        },
    }


def calculate_response_times(messages: list[PreparedMessage], participant_ids: tuple[int, int]) -> dict[int, list[float]]:
    """Calcula os tempos de resposta entre mensagens consecutivas de participantes diferentes."""
    response_times = {participant_id: [] for participant_id in participant_ids}

    for previous, current in zip(messages, messages[1:]):
        if previous.sender_id == current.sender_id:
            continue
        if current.sender_id not in response_times:
            continue

        delta_seconds = (current.sent_at - previous.sent_at).total_seconds()
        if delta_seconds >= 0:
            response_times[current.sender_id].append(delta_seconds)

    return response_times


def balance_score(first: float, second: float, neutral_when_empty: bool = False) -> float:
    """Calcula um score de equilíbrio entre dois valores, retornando um valor entre 0 e 100."""
    if first <= 0 and second <= 0:
        return 50.0 if neutral_when_empty else 100.0

    bigger = max(first, second)
    smaller = min(first, second)
    if bigger <= 0:
        return 0.0

    return max(0.0, min(100.0, (smaller / bigger) * 100))


def response_speed_score(seconds: list[float]) -> float:
    """Calcula um score de velocidade de resposta com base em tempos de resposta."""
    average = mean_or_none(seconds)
    if average is None:
        return 50.0
    if average <= 5 * 60:
        return 100.0
    if average <= 60 * 60:
        return 85.0
    if average <= 6 * 60 * 60:
        return 65.0
    if average <= 24 * 60 * 60:
        return 45.0
    return 25.0


def mean_or_zero(values: list[float | int]) -> float:
    """Calcula a média de uma lista de valores, retornando 0.0 se a lista estiver vazia."""
    if not values:
        return 0.0

    return float(mean_or_none(values))


def mean_or_none(values: list[float | int]) -> float | None:
    """Calcula a média de uma lista de valores, retornando None se a lista estiver vazia."""
    if not values:
        return None

    return float(mean(values))


def round_or_none(value: float | None) -> float | None:
    if value is None:
        return None

    return round(value, 2)

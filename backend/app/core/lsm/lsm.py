from __future__ import annotations
from collections import Counter
from app.core.preprocessing import PreparedMessage

WORD_CATEGORIES: dict[str, set[str]] = {
    "pronomes": {
        "eu",
        "tu",
        "voce",
        "vc",
        "voces",
        "ele",
        "ela",
        "eles",
        "elas",
        "nos",
        "me",
        "mim",
        "comigo",
        "te",
        "ti",
        "contigo",
        "se",
        "si",
        "lhe",
        "lhes",
        "isso",
        "isto",
        "aquilo",
        "quem",
        "qual",
        "quais",
    },
    "artigos": {
        "o",
        "a",
        "os",
        "as",
        "um",
        "uma",
        "uns",
        "umas",
    },
    "preposicoes": {
        "de",
        "do",
        "da",
        "dos",
        "das",
        "em",
        "no",
        "na",
        "nos",
        "nas",
        "por",
        "pelo",
        "pela",
        "pelos",
        "pelas",
        "para",
        "pra",
        "pro",
        "com",
        "sem",
        "sobre",
        "entre",
        "ate",
        "apos",
        "antes",
        "contra",
        "desde",
    },
    "conjuncoes": {
        "e",
        "ou",
        "mas",
        "porque",
        "pois",
        "porem",
        "contudo",
        "entretanto",
        "quando",
        "enquanto",
        "se",
        "que",
        "como",
        "embora",
        "tambem",
    },
    "negacoes": {
        "nao",
        "nem",
        "nunca",
        "jamais",
        "nada",
        "ninguem",
    },
    "auxiliares": {
        "ser",
        "sou",
        "e",
        "era",
        "foi",
        "sao",
        "estar",
        "estou",
        "esta",
        "estava",
        "estao",
        "ter",
        "tenho",
        "tem",
        "tinha",
        "haver",
        "ha",
        "vai",
        "vou",
        "vamos",
    },
    "adverbios_funcionais": {
        "ja",
        "ainda",
        "agora",
        "aqui",
        "ali",
        "la",
        "ca",
        "bem",
        "mal",
        "muito",
        "pouco",
        "mais",
        "menos",
        "so",
        "apenas",
        "talvez",
    },
    "quantificadores": {
        "todo",
        "toda",
        "todos",
        "todas",
        "cada",
        "algum",
        "alguma",
        "alguns",
        "algumas",
        "outro",
        "outra",
        "outros",
        "outras",
        "mesmo",
        "mesma",
    },
}


def count_categories(messages: list[PreparedMessage]) -> tuple[int, dict[str, int]]:
    tokens = [token for message in messages for token in message.canonical_tokens]
    token_counts = Counter(tokens)

    category_counts = {
        category: sum(token_counts[word] for word in words)
        for category, words in WORD_CATEGORIES.items()
    }
    return len(tokens), category_counts


def ratio(count: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return count / total


def category_lsm(first_ratio: float, second_ratio: float) -> float | None:
    if first_ratio == 0 and second_ratio == 0:
        return None
    return 1 - (abs(first_ratio - second_ratio) / (first_ratio + second_ratio + 0.0001))


def calculate_lsm(messages: list[PreparedMessage], participant_ids: tuple[int, int]) -> dict:
    first_id, second_id = participant_ids
    first_messages = [message for message in messages if message.sender_id == first_id]
    second_messages = [message for message in messages if message.sender_id == second_id]

    totals = {}
    category_counts_by_user = {}
    category_ratios_by_user = {}

    for participant_id, participant_messages in ((first_id, first_messages), (second_id, second_messages)):
        total_tokens, category_counts = count_categories(participant_messages)
        totals[participant_id] = total_tokens

        category_counts_by_user[participant_id] = category_counts
        category_ratios_by_user[participant_id] = {
            category: ratio(count, total_tokens)
            for category, count in category_counts.items()
        }

    category_scores: dict[str, float | None] = {}
    active_scores: list[float] = []

    for category in WORD_CATEGORIES:
        first_ratio = category_ratios_by_user[first_id][category]
        second_ratio = category_ratios_by_user[second_id][category]
        category_score = category_lsm(first_ratio, second_ratio)

        if category_score is None:
            category_scores[category] = None
            continue

        score = round(max(0.0, min(1.0, category_score)) * 100, 2) # score 0-100
        category_scores[category] = score
        active_scores.append(score)

    score = round(sum(active_scores) / len(active_scores), 2) if active_scores else 50.0

    return {
        "score": score,
        "active_categories": len(active_scores),
        "category_scores": category_scores,
        "participants": {
            str(participant_id): {
                "token_count": totals[participant_id],
                "category_counts": category_counts_by_user[participant_id],
                "category_ratios": {
                    category: round(value, 4)
                    for category, value in category_ratios_by_user[participant_id].items()
                },
            }
            for participant_id in participant_ids
        },
    }

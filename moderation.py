# moderation.py
import re

# Root-based matching covers most inflections without listing every form
_PROFANITY_ROOTS = [
    "хуй", "хуя", "хуе", "хую",
    "пизд",
    "ебат", "ебан", "наеб", "выеб", "заеб", "отеб", "ебл",
    "бляд", "блять",
    "мудак", "мудил",
    "залуп",
    "шлюх",
    "пидор", "пидар",
    "ублюдок",
    "долбоёб", "долбоеб",
    "говнюк",
]

_OFFTOPIC_KEYWORDS = [
    "крипт", "биткоин", "bitcoin", "ethereum", "nft",
    "казино", "ставк", "азартн",
    "займ", "кредит", "ипотек",
    "порно", "эротик", "секс-",
    "реклам", "спам",
]

_RESPONSE_PROFANITY = (
    "Давайте общаться в деловом тоне — тогда смогу помочь. "
    "Напишите ответ без нецензурных слов."
)

_RESPONSE_OFFTOPIC = (
    "Это за рамками нашей темы. "
    "Я здесь, чтобы разобраться с задачами по ИИ и автоматизации — "
    "давайте вернёмся к вопросу."
)


def _normalize(text: str) -> str:
    """Lowercase and strip spaces to catch split-word tricks."""
    return re.sub(r"\s+", "", text.lower())


def check(text: str) -> str | None:
    """
    Return a reply string if the message violates moderation rules,
    or None if the message is clean.
    """
    normalized = _normalize(text)
    lower = text.lower()

    if any(root in normalized for root in _PROFANITY_ROOTS):
        return _RESPONSE_PROFANITY

    if any(kw in lower for kw in _OFFTOPIC_KEYWORDS):
        return _RESPONSE_OFFTOPIC

    return None
